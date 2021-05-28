from unittest import skip
import datetime

from django.test import TestCase, Client
from django.http import HttpRequest
from django.urls import reverse, reverse_lazy

from todo.models import Project, Tag, Task
from todo.views import index

class TestIndexView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.c = Client()

    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_html(self):
        request = HttpRequest()
        response = index(request)
        html = response.content.decode('utf8')
        html_title = '<title>Task Complete</title>'
        html_doctype = '\n<!DOCTYPE html>\n'
        self.assertIn(html_title, html)
        self.assertTrue(html.startswith(html_doctype))
        self.assertEqual(response.status_code, 200)


class ProjectListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.c = Client()

        # Create 5 projects
        number_of_projects = 5
        for project in range(number_of_projects):
            Project.objects.create(
                title='Portfolio', 
                description='Tasks to complete portfolio website'
                )

    def test_view_url_exists_at_desired_location(self):
        response = self.c.get('/projects/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.c.get(reverse('projects'))
        self.assertEqual(response.status_code, 200)


class TestProjectTaskListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.c = Client()

        # Create 5 projects
        number_of_projects = 5
        for project in range(number_of_projects):
            Project.objects.create(
                title='Portfolio', 
                description='Tasks to complete portfolio website'
                )
    
    def test_view_url_exists_at_desired_location(self):
        id = Project.objects.values_list('id')[0][0]
        url = '/project/' + str(id)
        response = self.c.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        id = Project.objects.values_list('id')[0][0]
        response = self.c.get(reverse('project-task-list', args=[str(id)]))
        self.assertEqual(response.status_code, 200)

    
class TestTaskDeleteView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.c = Client()

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

    def test_get_success_url(self):
        task = self.test_task
        project_id = task.project_id
        url = reverse_lazy('project-task-list', kwargs={'pk': project_id})
        response = self.c.post(reverse('task-delete', kwargs={'pk': task.id}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(url, f'/project/{project_id}')
        self.assertRedirects(response, url)