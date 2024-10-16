from rest_framework.permissions import BasePermission

class IsModerator(BasePermission):
    """
    Этот класс проверяет, является ли юзер модератором. Если юзер принадлежит группе 'moderators', то
    он может получить доступ.
    """
    def has_permission(self, request, view):
        # Проверяем, есть ли у пользователя группа с названием 'moderators'.
        return request.user.groups.filter(name='moderators').exists()

class IsOwner(BasePermission):
    """
    Этот класс разрешает владельцу объекта делать с ним что угодно. Другие юзеры могут только просматривать объект
    (т.е. делать запросы GET).
    """
    def has_object_permission(self, request, view, obj):
        # Если пользователь — владелец объекта, то тоже разрешаем доступ.
        return obj.user == request.user  # Позволяет менять только тот объект, который принадлежит пользователю.