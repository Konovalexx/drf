from django.core.management.base import BaseCommand
from users.models import User, Payment
from courses.models import Course
import random
from faker import Faker


class Command(BaseCommand):
    help = 'Заполняет базу данных случайными данными о платежах'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Получаем всех пользователей и курсы
        users = User.objects.all()
        courses = Course.objects.all()

        for _ in range(10):  # Создадим 10 случайных платежей
            user = random.choice(users)
            course = random.choice(courses)
            amount = random.uniform(10.00, 1000.00)  # Случайная сумма от 10 до 1000
            payment_date = fake.date_time_this_year()

            Payment.objects.create(
                user=user,
                payment_date=payment_date,
                course=course,
                amount=amount,
                payment_method=random.choice(['cash', 'transfer'])
            )

        self.stdout.write(self.style.SUCCESS('Успешно заполнено 10 платежей.'))