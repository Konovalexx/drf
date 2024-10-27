from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView  # Импортируем RedirectView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Настройка представления для документации
schema_view = get_schema_view(
    openapi.Info(
        title="Ваш API",
        default_version='v1',
        description="Тестовое описание вашего API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),  # Включает маршрут для административной панели
    path('users/', include('users.urls')),  # Включает URL-адреса приложения пользователей
    path('courses/', include('courses.urls')),  # Включает URL-адреса приложения курсов
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # URL для Swagger UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # URL для ReDoc
    path('', RedirectView.as_view(url='/swagger/', permanent=False)),  # Перенаправление на Swagger
]