from rest_framework import serializers
from .models import User, Payment


class UserSerializer(serializers.ModelSerializer):
    # Поле для отображения количества платежей
    payment_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'is_active', 'is_staff', 'payment_count']

    def get_payment_count(self, obj):
        return obj.payment_set.count()  # Количество платежей для данного пользователя


class PaymentSerializer(serializers.ModelSerializer):
    # Используем вложенные сериализаторы для курсов и уроков
    user = serializers.StringRelatedField()  # Отображаем email пользователя
    course = serializers.StringRelatedField()  # Отображаем строковое представление курса
    lesson = serializers.StringRelatedField()  # Отображаем строковое представление урока

    class Meta:
        model = Payment
        fields = ['id', 'user', 'payment_date', 'course', 'lesson', 'amount', 'payment_method']

    def validate_amount(self, value):
        """Проверка на положительность суммы оплаты"""
        if value <= 0:
            raise serializers.ValidationError("Сумма оплаты должна быть положительной.")
        return value

    def create(self, validated_data):
        """Дополнительная логика при создании платежа (если нужно)"""
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Дополнительная логика при обновлении платежа (если нужно)"""
        return super().update(instance, validated_data)