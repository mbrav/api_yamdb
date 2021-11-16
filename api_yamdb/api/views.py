from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters import CharFilter, FilterSet, NumberFilter
from django_filters.filters import NumberFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from reviews.models import Category, Genre, Review, Title

from .permissions import (IsAdminOrReadOnly, IsAdminUser,
                          IsAuthorOrReadOnlyPermission, ReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitlePostSerializer, TitleSerializer)

User = get_user_model()


class TitleFilterBackend(FilterSet):
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')
    year = NumberFilter(field_name='year')
    name = CharFilter(field_name='name', lookup_expr='icontains')


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = TitleFilterBackend
    filterset_fields = ('genre', 'category', 'year', 'name',)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializer

        return TitlePostSerializer

    def perform_create(self, serializer):
        serializer.save()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUser,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def retrieve(self, request, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, **kwargs):
        slug = self.kwargs.get('pk')
        instance = get_object_or_404(Genre, slug=slug)
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
        return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, **kwargs):
        slug = self.kwargs.get('pk')
        instance = get_object_or_404(Category, slug=slug)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        new_queryset = Review.objects.filter(title=title)
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True

        # Проверяем юзера и автора ревью
        # Если у юзера роль 'user' и автор ревью не он
        # Даем ему 403
        instance = self.get_object()
        user = request.user
        review_user = instance.author
        if user.role == 'user' and review_user != user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Если у юзера роль 'user' и он хочет удалить ревью
        # Даем ему 403
        instance = self.get_object()
        user = request.user
        if user.role == 'user':
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, id=review_id)

    def req_user(self):
        return self.request.user

    def get_queryset(self):
        review = self.review()
        commments = review.comments.all()
        return commments

    def perform_create(self, serializer):
        if self.req_user().is_authenticated is False:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        review = self.review()
        serializer.save(author=self.request.user, review=review)

    def perform_update(self, serializer):
        user = self.req_user()
        instance = self.get_object()
        auth = user.is_authenticated
        if not auth:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if user.role == 'user' and instance.author != user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        # Если у юзера роль 'user' и он хочет удалить коммент
        # Даем ему 403
        instance = self.get_object()
        user = self.req_user()
        auth = user.is_authenticated
        if user.role == 'user' or not auth:
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
