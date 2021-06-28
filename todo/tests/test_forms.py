import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from ..forms import ProjectForm, TaskForm
from ..models import Project, Task


class TaskFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create(username='john', email='john@example.com')
        cls.test_user.set_password('mysecret')
        cls.test_user.save()
        test_project = Project.objects.create(
            title='Portfolio',
            description='Tasks to complete portfolio website',
            user=cls.test_user
            )
        cls.test_task = Task.objects.create(
            title='Create site map',
            project_id=test_project.id,
            priority=3,
            due_date=datetime.date.today() + datetime.timedelta(days=14),
            note='Lorem ipsum dolor sit amet.',
            complete=False
            )

    def test_valid_form(self):
        self.client.force_login(self.test_user)
        data = {
            'title': self.test_task.title,
            'project': self.test_task.project.pk,
            'priority': self.test_task.priority,
            'due_date': self.test_task.due_date,
            'note': self.test_task.note,
        }

        form = TaskForm(data=data, user=self.test_user)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        self.client.force_login(self.test_user)
        data = {
            'title': '',
            'project': self.test_task.project.pk,
            'priority': self.test_task.priority,
            'due_date': self.test_task.due_date,
            'note': self.test_task.note,
        }

        form = TaskForm(data=data, user=self.test_user)
        self.assertFalse(form.is_valid())


class ProjectFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create(
            username='john',
            email='john@example.com'
            )
        cls.test_user.set_password('mysecret')
        cls.test_user.save()
        cls.test_project = Project.objects.create(
            title='Portfolio',
            description='Tasks to complete portfolio website',
            user=cls.test_user
            )

    def test_valid_form(self):
        self.client.force_login(self.test_user)
        data = {
            'title': self.test_project.title,
            'description': self.test_project.description
        }

        form = ProjectForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        self.client.force_login(self.test_user)
        data = {
            'title': '',
            'description': self.test_project.description
        }

        form = ProjectForm(data=data)
        self.assertFalse(form.is_valid())
