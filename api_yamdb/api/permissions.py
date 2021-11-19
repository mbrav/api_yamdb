from rest_framework import permissions


class IsAuthorOrReadOnlyPermission(permissions.IsAuthenticatedOrReadOnly):

    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

    def has_permission(self, request, view):

        if request.method == 'DELETE':
            return request.user and request.user.is_authenticated

        return bool(
            request.method in self.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """"
        Проверка разрешения на объект 
        """

        auth = bool(request.user and request.user.is_authenticated)
        if not auth:
            return request.method in self.SAFE_METHODS

        is_owner = obj.author == request.user
        if request.method == 'DELETE':
            return is_owner or request.user.is_stf

        return bool(
            request.user.is_admin
            or is_owner
            and request.user
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

        test = view.action, request.method
        SAFE_ACTIONS = ('retrieve', 'partial_update',
                        'destroy', 'me')
        SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
        auth = bool(request.user and request.user.is_authenticated)
        if not auth:
            return False

        if view.action in SAFE_ACTIONS and request.user.is_usr or request.user.is_admin:
            return True
        return request.user.is_admin or request.user.is_mod

    def has_object_permission(self, request, view, obj):
        """"
        Проверка разрешения на объект User
        Только админа имеют право на просмотр других пользователей,
        кроме самого себя.
        """

        user = request.user
        is_owner = obj == user

        # Пользователь с ролью 'user' может изменять свою
        # информацию только через слаг 'me' а не через слаг
        # своего юзернейма
        if request.method == 'PATCH' and view.action != 'me' and user.is_usr:
            return False

        # Все пользователи не имеют право совершать суицид
        # от своего имени, не зависимо от статуса
        if request.method == 'DELETE' and view.action == 'me':
            return False

        # Только админы имеют право убивать
        if request.method == 'DELETE':
            return user.is_admin

        return user.is_admin or is_owner
