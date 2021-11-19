from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

from api.permissions import IsAdminUserOrOwner

from .serializers import (RegisterSerializer, UserCreateSerializer,
                          UserLoginSerializer, UserSerializer)
from .utils import Util

User = get_user_model()


class YamDBRegisterView(generics.CreateAPIView):
    """
    Вюшка для получения confirmation_code.

    Токен проходит в Терминал через
    django.core.mail.backends.console.EmailBackend
    """

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

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
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers)


class YamDBTokenRefreshView(generics.RetrieveAPIView):
    """
    Вюшка для подтверждения confirmation_code
    и выдачи токена.
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.data['username']
        conf_code = serializer.data['confirmation_code']
        user = get_object_or_404(User, username=username)

        if (user is not None
                and Util.token_generator.check_token(user, conf_code)):
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


class UserViewSet(viewsets.ModelViewSet):
    """
    Вюшка для Users.
    """

    queryset = User.objects.all()
    permission_classes = (IsAdminUserOrOwner,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)

    @action(detail=False, methods=['patch', 'get'])
    def me(self, request):
        user = get_object_or_404(User, id=request.user.id)

        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            # Проверка на попытку пользователь с ролью 'user'
            # на эскалацию своего статуса через изменение поля 'role'
            # на что-тo кроме значения 'user'
            if (user.is_usr
                    and serializer.validated_data.pop(
                        'role', 'user')
                    != user.USER):
                return Response(
                    serializer.data,
                    status=status.HTTP_403_FORBIDDEN)
            self.perform_update(serializer)
            return Response(serializer.data)

    def get_serializer_class(self):
        # Кастомный сериалайзер для POST
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer
