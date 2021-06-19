import datetime

from django.test import TestCase
from django.urls.base import reverse

from ..models import Project, Task


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

    def test_project_url(self):
        """
        Test project id and URL reverse
        """
        project = self.test_project
        response = self.client.post(
            reverse("project-task-list", args=[str(project.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(project.get_absolute_url(), reverse("project-task-list", args=[str(project.id)]))


# class TestTagModel(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.test_tag = Tag.objects.create(name='design')

#     def test_object_name_is_name(self):
#         """
#         Test Tag object string is equal to name
#         """
#         tag = self.test_tag
#         expected_object_name = tag.name
#         self.assertTrue(isinstance(tag, Tag))
#         self.assertEqual(expected_object_name, str(tag))


class TestTaskModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_project = Project.objects.create(title='Portfolio', description='Tasks to complete portfolio website')
        # test_tag = Tag.objects.create(name='design')
        
        cls.test_task = Task.objects.create(
            title='Create site map', 
            project_id=test_project.id, 
            priority=3, 
            due_date=datetime.date.today() + datetime.timedelta(days=14), 
            note='Lorem ipsum dolor sit amet.',
            complete=False
            )

        # cls.test_task.tag.set([test_tag])

    def test_object_name_is_title(self):
        """
        Test Task object string is equal to title
        """
        
        task = self.test_task
        expected_object_name = task.title
        self.assertTrue(isinstance(task, Task))
        self.assertEqual(expected_object_name, str(task))

    def test_task_url(self):
        """
        Test task project id and URL reverse
        """
        task = self.test_task
        response = self.client.post(
            reverse("project-task-list", args=[str(task.project_id)]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(task.get_absolute_url(), reverse("project-task-list", args=[str(task.project_id)]))

    def test_tasks_custom_manager(self):
        tasks = Task.tasks.all()
        self.assertEqual(tasks.count(), 1)
