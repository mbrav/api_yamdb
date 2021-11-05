from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from rest_framework import permissions
from api.permissions import IsAuthorOrReadOnlyPermission
from rest_framework.pagination import LimitOffsetPagination
from .models import Review
from api.serializers import CommentSerializer


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


