from rest_framework import generics
from .models import User
from .serializers import UserSerializer

# Представление для получения списка пользователей и создания нового пользователя
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Представление для получения, обновления или удаления конкретного пользователя
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer