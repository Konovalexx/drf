from rest_framework import serializers
from .models import User, Payment

class UserSerializer(serializers.ModelSerializer):
    payment_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'is_active', 'is_staff', 'payment_count']

    def get_payment_count(self, obj):
        return obj.payment_set.count()


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    course = serializers.StringRelatedField()
    lesson = serializers.StringRelatedField()

    class Meta:
        model = Payment
        fields = ['id', 'user', 'payment_date', 'course', 'lesson', 'amount', 'payment_method']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Сумма оплаты должна быть положительной.")
        return value

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


# Новый сериализатор для создания продукта в Stripe
class ProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=512)


# Новый сериализатор для создания цены в Stripe
class PriceSerializer(serializers.Serializer):
    product_id = serializers.CharField(max_length=255)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)


# Новый сериализатор для создания сессии оформления заказа в Stripe
class CheckoutSessionSerializer(serializers.Serializer):
    price_id = serializers.CharField(max_length=255)
    success_url = serializers.URLField()
    cancel_url = serializers.URLField()