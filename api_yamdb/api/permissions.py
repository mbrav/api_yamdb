from rest_framework import permissions


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
                request.user.is_authenticated
                and request.user.role == 'admin'):
            return True


class IsAdminUser(permissions.IsAdminUser):
    """"Старое Кастомное разрешение для объектов User."""

    def has_permission(self, request, view):
        auth = bool(request.user and request.user.is_authenticated)
        if not auth:
            return False

        return bool(request.user and request.user.is_admin)


class IsAdminUserOrOwner(permissions.BasePermission):
    """"Кастомное разрешение для объектов User"""

    def has_permission(self, request, view):
        """"
        Проверка на разрешения делать определенные действия
        Без тщательной проверки, доступ к объектам закрыт.
        """

        auth = bool(request.user and request.user.is_authenticated)
        if not auth:
            return False
        action, user = view.action, request.user
        if (action in ['retrieve', 'partial_update', 'destroy']
                and user.role in ['user', 'moderator']):
            return True
        return bool(request.user and user.is_admin)

    def has_object_permission(self, request, view, obj):
        """"
        Проверка разрешения на объект User
        Только админа имеют право на просмотр других пользователей,
        кроме самого себя.
        """

        user = request.user
        is_owner = obj == user
        return user.is_admin or is_owner
