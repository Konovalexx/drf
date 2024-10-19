from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import validate_video_url

class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[validate_video_url])  # Добавлен валидатор для поля video_url

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_url', 'course']

class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()  # Добавлено поле для проверки подписки

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'user', 'lesson_count', 'lessons', 'is_subscribed']

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user  # Получаем пользователя из контекста запроса
        return Subscription.objects.filter(user=user, course=obj).exists()  # Проверяем наличие подписки


class SubscriptionSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)  # Добавим название курса в сериализатор

    class Meta:
        model = Subscription
        fields = ['id', 'user', 'course', 'course_title']  # Указываем необходимые поля для сериализации