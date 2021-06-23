import datetime

from django.test import TestCase
from django.urls.base import reverse
from django.contrib.auth.models import User

from ..models import Project, Task


class TestProjectModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create(username='john', email='john@example.com')
        cls.test_user.set_password('mysecret')
        cls.test_user.save()
        cls.test_project = Project.objects.create(title='Portfolio', description='Tasks to complete portfolio website', user=cls.test_user)

    def test_object_name_is_title(self):
        """
        Test Project object string is equal to title
        """
        self.client.force_login(self.test_user)
        project = self.test_project
        expected_object_name = project.title
        self.assertTrue(isinstance(project, Project))
        self.assertEqual(expected_object_name, str(project))

    def test_project_url(self):
        """
        Test project id and URL reverse
        """
        self.client.force_login(self.test_user)
        project = self.test_project
        response = self.client.post(
            reverse("project-task-list", args=[str(project.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(project.get_absolute_url(), reverse("project-task-list", args=[str(project.id)]))


class TestTaskModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create(username='john', email='john@example.com')
        cls.test_user.set_password('mysecret')
        cls.test_user.save()
        test_project = Project.objects.create(title='Portfolio', description='Tasks to complete portfolio website', user=cls.test_user)
        
        cls.test_task = Task.objects.create(
            title='Create site map', 
            project_id=test_project.id, 
            priority=3, 
            due_date=datetime.date.today() + datetime.timedelta(days=14), 
            note='Lorem ipsum dolor sit amet.',
            complete=False
            )


    def test_object_name_is_title(self):
        """
        Test Task object string is equal to title
        """
        self.client.force_login(self.test_user)
        task = self.test_task
        expected_object_name = task.title
        self.assertTrue(isinstance(task, Task))
        self.assertEqual(expected_object_name, str(task))

    def test_task_url(self):
        """
        Test task project id and URL reverse
        """
        self.client.force_login(self.test_user)
        task = self.test_task
        response = self.client.post(
            reverse("project-task-list", args=[str(task.project_id)]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(task.get_absolute_url(), reverse("project-task-list", args=[str(task.project_id)]))

    def test_tasks_custom_manager(self):
        self.client.force_login(self.test_user)
        tasks = Task.tasks.all()
        self.assertEqual(tasks.count(), 1)
