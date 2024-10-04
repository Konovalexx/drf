from django.urls import path, include

urlpatterns = [
    path('users/', include('users.urls')),  # Включает URL-адреса приложения пользователей
    path('courses/', include('courses.urls')),  # Включает URL-адреса приложения курсов
]