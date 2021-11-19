from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters import CharFilter, FilterSet, NumberFilter
from django_filters.filters import NumberFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
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
        Genre.objects.filter(slug=slug).delete()
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
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, **kwargs):
        slug = self.kwargs.get('pk')
        Category.objects.filter(slug=slug).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

# Неплохо сократили тут


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def review(self):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Review, id=review_id, title_id=title_id)

    def get_queryset(self):
        review = self.review()
        comments = review.comments.all()
        return comments

    def perform_create(self, serializer):
        review = self.review()
        serializer.save(author=self.request.user, review=review)

# Неплохо сократили тут
