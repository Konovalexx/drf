from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from .models import User, Payment
from .serializers import UserSerializer, PaymentSerializer

# Представление для получения списка пользователей и создания нового пользователя
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Представление для получения, обновления или удаления конкретного пользователя
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Вьюсет для управления платежами
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']  # Поля для фильтрации
    ordering_fields = ['payment_date']  # Поля для упорядочивания
    ordering = ['-payment_date']  # Сортировка по умолчанию - сначала новые