from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination

from .serializers import (
    CommentSerializer, TitleSerializer,
    GenreSerializer, CategorySerializer, ReviewSerializer
)
from .permissions import (IsAuthorOrReadOnlyPermission,
                          ReadOnly, CustomPermission)
from reviews.models import Category, Title, Genres, Review

User = get_user_model()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (CustomPermission, IsAuthorOrReadOnlyPermission)
    pagination_class = LimitOffsetPagination,

    def review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, id=review_id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.review)

    def get_queryset(self):
        return self.review.comments.all()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination,

    def title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        return self.title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.title)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
