from django.db import models
from users.models import User

class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название курса")
    preview = models.ImageField(upload_to='course_previews/', verbose_name="Превью курса", blank=True, null=True)
    description = models.TextField(verbose_name="Описание курса", blank=True)
    user = models.ForeignKey(User, related_name='courses', on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ['title']

    def __str__(self):
        return self.title

class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название урока")
    description = models.TextField(verbose_name="Описание урока", blank=True)
    preview = models.ImageField(upload_to='lesson_previews/', verbose_name="Превью урока", blank=True, null=True)
    video_url = models.URLField(verbose_name="Ссылка на видео", blank=True)
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE, verbose_name="Курс")
    user = models.ForeignKey(User, related_name='lessons', on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ['title']

    def __str__(self):
        return self.title