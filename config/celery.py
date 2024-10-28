from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Задаем переменную окружения для настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создаем экземпляр Celery с именем проекта
app = Celery('config')

# Загружаем настройки из конфигурации Django, используя префикс "CELERY"
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находит и регистрирует задачи в приложениях
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')