from rest_framework import routers

from django.urls import path, include
from ..views import CommentViewSet, ReviewViewSet

router = routers.DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='titles'
)

urlpatterns = [
    path('', include(router.urls)),
]
