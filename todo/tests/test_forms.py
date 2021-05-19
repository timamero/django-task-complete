import datetime

from django.test import TestCase
from django.forms.widgets import Input
from django.http import HttpRequest

from ..models import Project, Task, Tag
from ..forms import TaskForm
from ..views import TaskDeleteView

class TaskFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_project = Project.objects.create(title='Portfolio', description='Tasks to complete portfolio website')
        test_tag = Tag.objects.create(name='design')
        cls.test_task = Task.objects.create(
            title='Create site map', 
            project_id=test_project.id, 
            priority=3, 
            due_date=datetime.date.today() + datetime.timedelta(days=14), 
            note='Lorem ipsum dolor sit amet.',
            complete=False
            )

        cls.test_task.tag.set([test_tag])
        cls.test_tag_id = test_tag.id
    
    def test_valid_form(self):
        data = {
            'title': self.test_task.title, 
            'project': self.test_task.project.pk, 
            'priority': self.test_task.priority,
            'due_date': self.test_task.due_date, 
            'note': self.test_task.note,
            'tag': [self.test_tag_id],
        }

        form = TaskForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            'title': '', 
            'project': self.test_task.project.pk, 
            'priority': self.test_task.priority,
            'due_date': self.test_task.due_date, 
            'note': self.test_task.note,
            'tag': [self.test_tag_id],
        }

        form = TaskForm(data=data)
        self.assertFalse(form.is_valid())
