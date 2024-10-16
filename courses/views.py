from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsModerator, IsOwner

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in self.permission_classes]


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.request.method == 'POST':  # Создание урока
            self.permission_classes = [IsAuthenticated, ~IsModerator]  # Не авторизованный пользователь не может создавать уроки
        return [permission() for permission in self.permission_classes]  # Просмотр для всех авторизованных

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.request.method in ['PUT', 'PATCH']:  # Редактирование
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.request.method == 'DELETE':
            self.permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in self.permission_classes]  # Просмотр для всех авторизованных