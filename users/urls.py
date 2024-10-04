from django.urls import path
from .views import UserListCreateView, UserDetailView

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user-list-create'),  # Эндпоинт для списка пользователей
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),  # Эндпоинт для конкретного пользователя
]