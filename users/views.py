import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import User, Payment, Course
from .serializers import UserSerializer, PaymentSerializer


# Настройка Stripe
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


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


# Вьюха для создания продукта в Stripe
class CreateProductView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        title = request.data.get('title')
        description = request.data.get('description')

        product = stripe.Product.create(
            name=title,
            description=description,
        )

        return Response(product)


# Вьюха для создания цены в Stripe
class CreatePriceView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        amount = request.data.get('amount')  # Укажите сумму в центах
        currency = request.data.get('currency', 'usd')

        price = stripe.Price.create(
            unit_amount=amount,
            currency=currency,
            product=product_id,
        )

        return Response(price)


# Вьюха для создания сессии оформления заказа в Stripe
class CreateCheckoutSessionView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        # Получите цену для курса, здесь вы можете использовать вашу логику
        price_id = request.data.get('price_id')

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://your-success-url.com',
            cancel_url='https://your-cancel-url.com',
        )

        return Response({'id': session.id})