from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from .models import User, Payment
from .serializers import UserSerializer, PaymentSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView


# Вьюха показа списка пользователей и создания новых пользователей
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # Разрешаем просмотр списка только аутентифицированным пользователям
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        # Создание пользователя доступно без аутентификации (например, для регистрации)
        return []


# Вьюха для получения, обновления или удаления пользователя по ID
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # Обновление и удаление разрешено только самому пользователю или админу
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsAdminUser()]  # Либо можно сделать проверку на владельца
        return [IsAuthenticated()]


# Вьюсет для работы с платежами, КРУД
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # Только админ или сам пользователь, связанный с платежом, могут видеть/редактировать
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]  # Все аутентифицированные пользователи могут видеть
        return [IsAdminUser()]  # Только админ может создавать/удалять платежи