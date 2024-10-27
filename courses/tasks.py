from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_update_email(user_email, course_name):
    send_mail(
        f'Обновление курса: {course_name}',
        'Курс был обновлен. Ознакомьтесь с новыми материалами!',
        'from@example.com',  # Укажите здесь реальный email-отправителя
        [user_email],
        fail_silently=False,
    )