
from django.contrib import admin
from .models import User, Payment

# Настройка админского интерфейса для кастомной модели пользователя
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'city', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'phone', 'city')
    ordering = ('email',)

# Настройка админского интерфейса для модели платежей
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_date', 'course', 'lesson', 'amount', 'payment_method')
    list_filter = ('payment_method', 'course', 'lesson')
    search_fields = ('user__email', 'amount')
    ordering = ('-payment_date',)

# Регистрация моделей в админке
admin.site.register(User, UserAdmin)
admin.site.register(Payment, PaymentAdmin)