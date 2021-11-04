from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import UserViewSet, TitleViewSet, CategoryViewSet, GenreViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'title', TitleViewSet, basename='title')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'genres', GenreViewSet, basename='genre')

urlpatterns = [
    path('v1/auth/signup/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/auth/token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/', include(router.urls)),
]
