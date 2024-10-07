from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserListCreateView, UserDetailView, PaymentViewSet

# Создаем экземпляр маршрутизатора
router = DefaultRouter()
router.register(r'payments', PaymentViewSet)  # Регистрация маршрута для платежей

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user-list-create'),  # Эндпоинт для списка пользователей
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),  # Эндпоинт для конкретного пользователя
    path('', include(router.urls)),  # Включаем маршруты платежей
]