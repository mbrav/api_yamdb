from rest_framework import permissions


class AllowAny(permissions.BasePermission):
    def has_permission(self, request, view):
        return True


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_superuser
        )


class ReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method == "GET"


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated and request.user.role == 'admin'):
            return True


class IsAdminUser(permissions.IsAdminUser):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        staff = request.user.is_staff or request.user.role == 'admin'
        return bool(request.user and staff)
