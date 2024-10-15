from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsModerator, IsOwnerOrReadOnly, IsAuthenticatedAndNotModerator

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method == 'POST':  # Создание курса
            return [IsAuthenticatedAndNotModerator()]  # Не авторизованный пользователь не может создавать курс
        elif self.request.method in ['DELETE']:  # Удаление курса
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        elif self.request.method in ['PUT', 'PATCH']:  # Редактирование курса
            return [IsAuthenticated(), IsOwnerOrReadOnly() | IsModerator()]
        return [IsAuthenticated()]  # Просмотр для всех авторизованных и анонимных

class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == 'POST':  # Создание урока
            return [IsAuthenticatedAndNotModerator()]  # Не авторизованный пользователь не может создавать уроки
        return [IsAuthenticated()]  # Просмотр для всех авторизованных и анонимных

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:  # Редактирование и удаление
            return [IsAuthenticated(), IsOwnerOrReadOnly() | IsModerator()]
        return [IsAuthenticated()]  # Просмотр для всех авторизованных и анонимных