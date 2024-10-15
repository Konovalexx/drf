from django.contrib import admin
from .models import Course, Lesson

# Настройка отображения курса в админке
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'lesson_count', 'created_at', 'updated_at')
    search_fields = ('title', 'user__email')  # Поиск по названию и почте пользователя
    list_filter = ('user',)  # Фильтрация по пользователю

    def lesson_count(self, obj):
        return obj.lessons.count()
    lesson_count.short_description = 'Количество уроков'

# Настройка отображения урока в админке
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'user', 'created_at', 'updated_at')
    search_fields = ('title', 'course__title', 'user__email')  # Поиск по названию, курсу и почте пользователя
    list_filter = ('course', 'user')  # Фильтрация по курсу и пользователю

# Регистрация моделей в админке
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)