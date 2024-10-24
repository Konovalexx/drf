from rest_framework import status, filters, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment, User
from .serializers import PaymentSerializer, UserSerializer
from .services import create_stripe_product, create_stripe_price, create_stripe_checkout_session
from rest_framework import generics

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
            return [IsAuthenticated(), IsAdminUser()]
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

    def perform_create(self, serializer):
        # Создаем платеж
        payment = serializer.save()

        # Получаем данные для создания продукта и цены в Stripe
        title = f"Платеж за курс {payment.course} или урок {payment.lesson}"
        description = f"Оплата за курс {payment.course} или урок {payment.lesson} от пользователя {payment.user.email}"

        # Создаем продукт в Stripe
        product = create_stripe_product(title, description)

        # Создаем цену в Stripe (сумма в центах)
        price = create_stripe_price(product.id, int(payment.amount * 100))

        # Создаем сессию оплаты
        session = create_stripe_checkout_session(
            price.id,
            'https://your-success-url.com',  # URL для успешной оплаты
            'https://your-cancel-url.com'    # URL для отмены
        )

        # Сохраняем ссылку на сессию в поле платежа
        payment.stripe_session_url = session.url
        payment.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)