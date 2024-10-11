from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonListCreateView, LessonDetailView

router = DefaultRouter()
# Регистрируем CourseViewSet, который включает маршруты для CRUD операций (list, create, retrieve, update, delete)
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    # Добавляем маршруты для курсов
    path('', include(router.urls)),
]