from rest_framework import serializers
from .models import User, Payment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'payment_date', 'course', 'lesson', 'amount', 'payment_method']