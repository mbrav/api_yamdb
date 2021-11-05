from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, YamDBRegisterView, YamDBTokenRefreshView
from .views import TitleViewSet, CategoryViewSet, GenreViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'title', TitleViewSet, basename='title')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'genres', GenreViewSet, basename='genre')

urlpatterns = [
    path('v1/auth/signup/', YamDBRegisterView.as_view(),
         name='token_obtain_pair'),
    path('v1/auth/token/', YamDBTokenRefreshView.as_view(), name='token_refresh'),
    path('v1/', include(router.urls)),
]
