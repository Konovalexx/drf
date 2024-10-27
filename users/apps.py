from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        # Импортируйте и вызовите функцию настройки периодических задач
        from .scheduler import setup_periodic_tasks
        setup_periodic_tasks()