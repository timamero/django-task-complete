import datetime

from django.test import TestCase

from ..models import Project, Tag, Task


class TestProjectModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_project = Project.objects.create(title='Portfolio', description='Tasks to complete portfolio website')

    def test_object_name_is_title(self):
        """
        Test Project object string is equal to title
        """
        project = self.test_project
        expected_object_name = project.title
        self.assertTrue(isinstance(project, Project))
        self.assertEqual(expected_object_name, str(project))


class TestTagModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_tag = Tag.objects.create(name='design')

    def test_object_name_is_name(self):
        """
        Test Tag object string is equal to name
        """
        tag = self.test_tag
        expected_object_name = tag.name
        self.assertTrue(isinstance(tag, Tag))
        self.assertEqual(expected_object_name, str(tag))


class TestTaskModel(TestCase):
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

    def test_object_name_is_title(self):
        """
        Test Task object string is equal to title
        """
        
        task = self.test_task
        expected_object_name = task.title
        self.assertTrue(isinstance(task, Task))
        self.assertEqual(expected_object_name, str(task))