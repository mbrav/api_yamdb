from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, status

from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .serializers import (
    CommentSerializer, TitleSerializer,
    GenreSerializer, CategorySerializer
)
from .permissions import (
    IsAuthorOrReadOnlyPermission, ReadOnly, IsAdminOrReadOnly)
from reviews.models import Category, Title, Genres

User = get_user_model()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.review)

    def review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, id=review_id)

    def get_queryset(self):
        return self.review.comments.all()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        print(serializer)
        serializer.save()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def retrieve(self, request, **kwargs):
        """ slug = self.kwargs.get('pk')
        instance = get_object_or_404(Category, slug=slug)
        serializer = CategorySerializer(instance)
        return Response(serializer.data) """
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def partial_update(self, request, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def destroy(self, request, **kwargs):
        slug = self.kwargs.get('pk')
        instance = get_object_or_404(Genres, slug=slug)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return (ReadOnly(),)
        return super().get_permissions()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    
    def retrieve(self, request, **kwargs):
        """ slug = self.kwargs.get('pk')
        instance = get_object_or_404(Category, slug=slug)
        serializer = CategorySerializer(instance)
        return Response(serializer.data) """
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def partial_update(self, request, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
    def destroy(self, request, **kwargs):
        slug = self.kwargs.get('pk')
        instance = get_object_or_404(Category, slug=slug)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    """ def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return (ReadOnly(),)
        return super().get_permissions() """
