from api.permissions import IsAuthorOrReadOnlyPermission, ReadOnly
from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .utils import Util
from django.core.mail import EmailMessage
from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()


class YamDBTokenRefreshView(TokenRefreshView):
    pass


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
        token = RefreshToken.for_user(user).access_token

        email_body = 'Добрый день, ' + \
            user.username + 'Ваш Токен: \n' + str(token)
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Verify your email'
        }
        Util.send_email(data)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
