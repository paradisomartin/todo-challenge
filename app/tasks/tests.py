from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Task, Tag

class TaskAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_create_task_with_title_and_tags(self):
        response = self.client.post('/api/tasks/', {
            'title': 'Test Task',
            'description': 'Test Description',
            'tags': ['Work', 'Important']
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Tag.objects.count(), 2)
        task = Task.objects.first()
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.description, 'Test Description')
        self.assertEqual(task.tags.count(), 2)
        self.assertEqual(task.user, self.user)
        self.assertEqual(set(response.data['tag_titles']), {'Work', 'Important'})

    def test_create_task_without_title(self):
        response = self.client.post('/api/tasks/', {
            'description': 'Task without title',
            'tags': []
        })
        self.assertEqual(response.status_code, 400)  # Bad Request

    def test_create_task_with_title_without_description(self):
        response = self.client.post('/api/tasks/', {
            'title': 'Task with title only'
        })
        self.assertEqual(response.status_code, 201)
        task = Task.objects.get(title='Task with title only')
        self.assertEqual(task.description, '')
        self.assertEqual(task.tags.count(), 0)
        self.assertEqual(task.user, self.user)

    def test_create_task_with_existing_tag(self):
        Tag.objects.create(title='Existing', user=self.user)
        response = self.client.post('/api/tasks/', {
            'title': 'Task with existing tag',
            'tags': ['Existing', 'New']
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tag.objects.count(), 2)
        task = Task.objects.get(title='Task with existing tag')
        self.assertEqual(task.tags.count(), 2)
        self.assertEqual(task.user, self.user)
        self.assertEqual(set(response.data['tag_titles']), {'Existing', 'New'})

    def test_user_cannot_see_others_tasks(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        Task.objects.create(title='Other user task', user=other_user)

        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_user_cannot_see_others_tags(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        Tag.objects.create(title='Other user tag', user=other_user)

        response = self.client.get('/api/tags/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
