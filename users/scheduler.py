from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

def setup_periodic_tasks():
    # Создаём расписание, если оно не существует
    schedule, created = IntervalSchedule.objects.get_or_create(every=1, period=IntervalSchedule.DAYS)

    # Проверяем, существует ли задача с именем 'Deactivate inactive users'
    if not PeriodicTask.objects.filter(name='Deactivate inactive users').exists():
        # Создаём задачу только если её ещё нет
        PeriodicTask.objects.create(
            interval=schedule,
            name='Deactivate inactive users',
            task='users.tasks.deactivate_inactive_users',  # Убедитесь, что имя задачи верное
        )