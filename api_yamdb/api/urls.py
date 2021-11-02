from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

router = DefaultRouter()
router.register(r'posts', UserViewSet, basename='posts')


urlpatterns = [
    path('v1/auth/token/', views.obtain_auth_token),
    path('v1/', include(router.urls)),
]
