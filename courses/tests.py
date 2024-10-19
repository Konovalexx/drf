from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from .models import Course, Lesson, Subscription

class CourseTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(email='admin@example.com', password='password', is_staff=True)
        self.normal_user = User.objects.create_user(email='user@example.com', password='password')
        self.course = Course.objects.create(title="Test Course", user=self.admin_user)

    def test_create_course(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('course-list')
        data = {'title': 'New Course', 'user': self.admin_user.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)

    def test_update_course(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('course-detail', args=[self.course.id])
        data = {'title': 'Updated Course'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, 'Updated Course')

    def test_retrieve_course(self):
        self.client.force_authenticate(user=self.normal_user)  # Поменяйте на нужного пользователя
        url = reverse('course-detail', args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.course.title)

    def test_delete_course(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('course-detail', args=[self.course.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)


class LessonTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(email='admin@example.com', password='password', is_staff=True)
        self.normal_user = User.objects.create_user(email='user@example.com', password='password')
        self.course = Course.objects.create(title="Test Course", user=self.admin_user)
        self.lesson = Lesson.objects.create(title="Test Lesson", course=self.course, user=self.admin_user)

    def test_create_lesson(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('lesson-list')
        data = {'title': 'New Lesson', 'course': self.course.id}  # Убедитесь, что user не требуется
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_update_lesson(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('lesson-detail', args=[self.lesson.id])
        data = {'title': 'Updated Lesson'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated Lesson')

    def test_retrieve_lesson(self):
        self.client.force_authenticate(user=self.admin_user)  # Аутентификация администратора
        url = reverse('lesson-detail', args=[self.lesson.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.lesson.title)

    def test_delete_lesson(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('lesson-detail', args=[self.lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class SubscriptionTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(email='admin@example.com', password='password', is_staff=True)
        self.normal_user = User.objects.create_user(email='user@example.com', password='password')
        self.course = Course.objects.create(title="Test Course", user=self.admin_user)

    def test_subscribe_to_course(self):
        self.client.force_authenticate(user=self.normal_user)
        url = reverse('subscription-list')  # Убедитесь, что ваш URL соответствует маршруту
        data = {'course': self.course.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), 1)

    def test_unsubscribe_from_course(self):
        self.client.force_authenticate(user=self.normal_user)
        subscription = Subscription.objects.create(user=self.normal_user, course=self.course)
        url = reverse('subscription-detail', args=[self.normal_user.id, self.course.id])  # Убедитесь, что ваш URL соответствует маршруту
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subscription.objects.count(), 0)