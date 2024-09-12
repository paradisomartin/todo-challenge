from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APIClient
from .models import Task, Tag
from freezegun import freeze_time

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

    def test_filter_tasks_by_completion_status(self):
        Task.objects.create(title='Completed Task', user=self.user, is_completed=True)
        Task.objects.create(title='Incomplete Task', user=self.user, is_completed=False)

        response = self.client.get('/api/tasks/?is_completed=true')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Completed Task')

        response = self.client.get('/api/tasks/?is_completed=false')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Incomplete Task')

    def test_filter_tasks_by_tag(self):
        task1 = Task.objects.create(title='Task with tag', user=self.user)
        task2 = Task.objects.create(title='Task without tag', user=self.user)
        tag = Tag.objects.create(title='TestTag', user=self.user)
        task1.tags.add(tag)

        response = self.client.get('/api/tasks/?tags__title=TestTag')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Task with tag')

    def test_toggle_task_completion(self):
        task = Task.objects.create(title='Test Task', user=self.user)
        self.assertFalse(task.is_completed)

        response = self.client.post(f'/api/tasks/{task.id}/toggle_completed/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['is_completed'])

        task.refresh_from_db()
        self.assertTrue(task.is_completed)

        response = self.client.post(f'/api/tasks/{task.id}/toggle_completed/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data['is_completed'])

        task.refresh_from_db()
        self.assertFalse(task.is_completed)

    @freeze_time("2024-09-12 12:00:00")
    def test_filter_tasks_by_creation_date(self):
        today = timezone.now().date()
        yesterday = today - timezone.timedelta(days=1)
        tomorrow = today + timezone.timedelta(days=1)

        with freeze_time("2024-09-11 12:00:00"):
            Task.objects.create(title='Yesterday Task', user=self.user)

        Task.objects.create(title='Today Task', user=self.user)

        with freeze_time("2024-09-13 12:00:00"):
            Task.objects.create(title='Tomorrow Task', user=self.user)

        response = self.client.get(f'/api/tasks/?created_at={today.isoformat()}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Today Task')
