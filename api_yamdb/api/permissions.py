from rest_framework import permissions


class IsAuthorOrReadOnlyPermission(permissions.IsAuthenticatedOrReadOnly):

    def has_permission(self, request, view):
        SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

        return bool(
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )


class ReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method == "GET"


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated
                and request.user.is_admin):
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

        SAFE_ACTIONS = ('retrieve', 'partial_update', 'destroy')

        auth = bool(request.user and request.user.is_authenticated)
        if not auth:
            return False
        if view.action in SAFE_ACTIONS:
            return True
        return bool(request.user and request.user.is_admin)

    def has_object_permission(self, request, view, obj):
        """"
        Проверка разрешения на объект User
        Только админа имеют право на просмотр других пользователей,
        кроме самого себя.
        """

        user = request.user
        is_owner = obj == user
        return user.is_admin or is_owner
