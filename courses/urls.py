from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonListCreateView, LessonDetailView, SubscriptionView, SubscriptionListView

router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    # Маршруты для уроков
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),

    # Маршрут для подписки на курс
    path('subscribe/', SubscriptionView.as_view(), name='subscribe'),

    # Маршрут для получения списка подписок
    path('subscriptions/', SubscriptionListView.as_view(), name='subscription-list'),

    # Маршрут для управления конкретной подпиской (отписка)
    path('subscriptions/<int:user_id>/<int:course_id>/', SubscriptionView.as_view(), name='subscription-detail'),

    # Включаем маршруты для курсов
    path('', include(router.urls)),
]