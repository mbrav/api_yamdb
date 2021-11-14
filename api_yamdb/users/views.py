from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets, filters
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from api.permissions import AllowAny, IsAdminUser, IsAdminUserOrOwner
from .serializers import (RegisterSerializer, UserLoginSerializer,
                          UserCreateSerializer, UserUpdateSerializer)
from .utils import Util

User = get_user_model()


class YamDBTokenRefreshView(generics.RetrieveAPIView):
    """
    Вюшка для получения confirmation_code.

    Токен проходит в Терминал через
    django.core.mail.backends.console.EmailBackend
    """

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.data['username']
        conf_code = serializer.data['confirmation_code']
        user = get_object_or_404(User, username=username)

        if user is not None and Util.token_generator.check_token(user, conf_code):
            # Делаем юзера активным
            user.is_active = True
            user.save()
        else:
            response = {
                'confirmation_code': 'Токен не валидный'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        token = Token.objects.get_or_create(user=user)
        response = {
            'token': token[0].key,
        }
        return Response(response, status=status.HTTP_200_OK)


class YamDBRegisterView(generics.CreateAPIView):
    """
    Вюшка для подтверждения confirmation_code
    и выдачи токена.
    """

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = Util.token_generator.make_token(user)

        email_body = 'Добрый день, ' + \
            user.username + '\n' + \
            'Ваш confirmation_code: \n' + \
            str(token)
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Ваш Токен YamDB!'
        }
        Util.send_email(data)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class UserViewSet(viewsets.ModelViewSet):
    """
    Вюшка для Users.
    """

    permission_classes = (IsAdminUserOrOwner,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)

    def get_queryset(self):
        is_staff = self.request.user.is_staff or self.request.user.role in [
            'admin', 'moderator']
        if is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(username=self.request.user.username)

    def get_object(self):
        queryset = self.get_queryset()
        username = self.kwargs.get(self.lookup_field)
        if username == 'me':
            username = self.request.user.username
        if username:
            obj = get_object_or_404(User, username=username)
            self.check_object_permissions(self.request, obj)
            return obj

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        user = request.user
        serializer.is_valid(raise_exception=True)

        # Пользователь с ролью 'user' может изменять свою
        # информацию только через слаг 'me' а не через слаг
        # своего юзернейма
        username = self.kwargs.get(self.lookup_field)
        if user.role == 'user' and username == user.username:
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)

        # Проверка на попытку пользователь с ролью 'user'
        # на эскалацию своего статуса через изменение поля 'role'
        # на что-тo кроме значения 'user'
        if user.role == 'user' and serializer.validated_data.pop('role', 'user') != 'user':
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)

        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Все пользователи не имеют право совершать суицид
        # от своего имени, не зависимо от статуса
        username = self.kwargs.get(self.lookup_field)
        if username == 'me':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        # Только админы имеют право убивать
        is_staff = request.user.is_staff or request.user.role in [
            'admin']
        if not is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        # Кастомные сериалайзеры для POST и PATCH
        request_action = self.get_serializer_context()[
            'request']._request.method
        if request_action != "POST":
            return UserUpdateSerializer
        return UserCreateSerializer
