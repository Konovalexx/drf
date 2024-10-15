from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsModerator(BasePermission):
    """
    Этот класс проверяет, является ли юзер модератором. Если юзер принадлежит группе 'moderators', то
    он может получить доступ.
    """
    def has_permission(self, request, view):
        # Проверяем, есть ли у пользователя группа с названием 'moderators'.
        return request.user.groups.filter(name='moderators').exists()

class IsOwnerOrReadOnly(BasePermission):
    """
    Этот класс разрешает владельцу объекта делать с ним что угодно. Другие юзеры могут только просматривать объект
    (т.е. делать запросы GET).
    """
    def has_object_permission(self, request, view, obj):
        # Если метод запроса — это один из безопасных (например, GET), то разрешаем доступ.
        if request.method in SAFE_METHODS:  # SAFE_METHODS включает GET, HEAD, OPTIONS
            return True
        # Если пользователь — владелец объекта, то тоже разрешаем доступ.
        return obj.user == request.user  # Позволяет менять только тот объект, который принадлежит пользователю.

class IsAuthenticatedAndNotModerator(BasePermission):
    """
    Этот класс проверяет, что пользователь вошел в систему и не является модером. Позволяет действовать только обычным
    юзерам, которые не модераторы.
    """
    def has_permission(self, request, view):
        # Проверяем, что пользователь авторизован и не находится в группе 'moderators'.
        return request.user.is_authenticated and not request.user.groups.filter(name='moderators').exists()