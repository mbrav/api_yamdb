from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser

from users.models import User

from .permissions import IsAuthorOrReadOnlyPermission, ReadOnly
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = (IsAdminUser,)
    pagination_class = LimitOffsetPagination
