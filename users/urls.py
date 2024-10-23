from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserListCreateView,
    UserDetailView,
    PaymentViewSet,
    CreateProductView,
    CreatePriceView,
    CreateCheckoutSessionView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Создаем роутер для Payments ViewSet
router = DefaultRouter()
router.register(r'payments', PaymentViewSet)

# Определяем URL-паттерны для регистрации, авторизации, обновления токена и CRUD пользователей
urlpatterns = [
    # Регистрация пользователя (ListCreate)
    path('register/', UserListCreateView.as_view(), name='user-list-create'),

    # Эндпоинт для детальной работы с пользователем (RetrieveUpdateDestroy)
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    # JWT Авторизация
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Включаем роуты для платежей (payments)
    path('', include(router.urls)),

    # Маршруты для Stripe
    path('create-product/', CreateProductView.as_view(), name='create-product'),
    path('create-price/', CreatePriceView.as_view(), name='create-price'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
]