from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Включает маршрут для административной панели
    path('users/', include('users.urls')),  # Включает URL-адреса приложения пользователей
    path('courses/', include('courses.urls')),  # Включает URL-адреса приложения курсов
]