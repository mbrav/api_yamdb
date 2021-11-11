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
        auth = bool(request.user and request.user.is_authenticated)
        if not auth:
            return False
        is_staff = request.user.is_staff or request.user.role in [
            'admin']
        return bool(request.user and is_staff)


class IsAdminUserOrOwner(IsAdminUser):
    def has_permission(self, request, view):
        auth = bool(request.user and request.user.is_authenticated)
        if not auth:
            return False
        action, user = view.action, request.user
        if action in ['retrieve', 'partial_update', 'destroy'] and user.role in [
                'user', 'moderator']:
            return True
        is_staff = user.is_staff or user.role in [
            'admin']
        return bool(request.user and is_staff)

    def has_object_permission(self, request, view, obj):
        action, user = view.action, request.user
        is_staff = user.is_staff or user.role in [
            'admin']
        is_owner = obj == user
        return is_staff or is_owner
