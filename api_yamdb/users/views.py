from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from .serializers import (RegisterSerializer, UserLoginSerializer,
                          UserSerializer)
from .utils import Util

User = get_user_model()


class YamDBTokenRefreshView(generics.RetrieveAPIView):
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
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
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
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
