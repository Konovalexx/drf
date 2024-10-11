from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Создает суперпользователя'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('phone', type=str)
        parser.add_argument('city', type=str)

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        phone = options['phone']
        city = options['city']

        User.objects.create_superuser(email=email, password=password, phone=phone, city=city)
        self.stdout.write(self.style.SUCCESS(f'Суперпользователь {email} успешно создан.'))