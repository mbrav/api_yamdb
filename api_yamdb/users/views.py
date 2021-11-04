from api.permissions import IsAuthorOrReadOnlyPermission, ReadOnly
from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework_simplejwt.views import TokenRefreshView

from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()


class YamDBTokenRefreshView(TokenRefreshView):
    pass


class YamDBRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
