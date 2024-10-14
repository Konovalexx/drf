from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.contrib.auth.models import BaseUserManager


# User Manager для кастомной модели пользователя
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Поле Email должно быть заполнено')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


# Модель пользователя
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    phone = models.CharField(max_length=15, verbose_name="Телефон")
    city = models.CharField(max_length=100, verbose_name="Город")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")

    is_staff = models.BooleanField(default=False, verbose_name="Статус персонала")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_superuser = models.BooleanField(default=False, verbose_name="Суперпользователь")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'city']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['email']

    def __str__(self):
        return self.email


# Модель платежей
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    payment_date = models.DateTimeField(verbose_name="Дата оплаты")

    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name="Оплаченный курс")
    lesson = models.ForeignKey('courses.Lesson', on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name="Оплаченный урок")

    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма оплаты")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты")

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"Платеж {self.user.email} на сумму {self.amount} ({self.payment_method})"