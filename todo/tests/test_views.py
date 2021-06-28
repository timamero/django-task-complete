from unittest import skip
import datetime

from django.test import TestCase, Client, RequestFactory
from unittest import skip
from django.http import HttpRequest
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User, AnonymousUser, Group

from todo.models import Project, Task
from todo.views import index, ProjectUpdateView, ProjectCreateView, ProjectDeleteView, TaskListView, TaskUpdateView, TaskCreateView, TaskDeleteView, CompletedTaskListView, UserSignUpView
from todo.forms import ProjectForm, UserSignUpForm

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
        cls.test_user = User.objects.create(username='john', email='john@example.com')
        cls.test_user.set_password('mysecret')
        cls.test_user.save()

        # Create 5 projects
        number_of_projects = 5
        for project in range(number_of_projects):
            Project.objects.create(
                title='Portfolio', 
                description='Tasks to complete portfolio website',
                user=cls.test_user
                )

    def test_view_url_exists_at_desired_location(self):
        self.c.force_login(self.test_user)
        response = self.c.get('/projects/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.c.force_login(self.test_user)
        response = self.c.get(reverse('projects'))
        self.assertEqual(response.status_code, 200)


class TestProjectTaskListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.c = Client()
        cls.test_user = User.objects.create(username='john', email='john@example.com')
        cls.test_user.set_password('mysecret')
        cls.test_user.save()
        cls.test_user2 = User.objects.create(username='jane', email='jane@example.com')
        cls.test_user2.set_password('mysecret2')
        cls.test_user2.save()

        cls.test_project = Project.objects.create(title='Portfolio', description='Tasks to complete portfolio website', user=cls.test_user)

        # Create 5 Tasks
        number_of_tasks = 5
        for task in range(number_of_tasks):
            Task.objects.create(
                title='Create site map', 
                project_id=cls.test_project.id, 
                priority=3, 
                due_date=datetime.date.today() + datetime.timedelta(days=14), 
                note='Lorem ipsum dolor sit amet.',
                complete=False
            )
    
    def test_view_url_exists_at_desired_location(self):
        self.c.force_login(self.test_user)
        id = self.test_project.id
        url = '/project/' + str(id)
        response = self.c.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.c.force_login(self.test_user)
        id = self.test_project.id
        response = self.c.get(reverse('project-task-list', args=[str(id)]))
        self.assertEqual(response.status_code, 200)

    def test_redirect_not_user_for_project(self):
        self.c.force_login(self.test_user2)
        id = self.test_project.id
        url = '/project/' + str(id)
        response = self.c.get(url)
        self.assertRedirects(response, '/account/login/?next=%s')


class TestProjectUpdateView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.test_user = User.objects.create(username='john', email='john@example.com')
        cls.test_user.set_password('mysecret')
        cls.test_user.save()

        cls.test_project = Project.objects.create(title='Portfolio', description='Tasks to complete portfolio website', user=cls.test_user)

    def test_test_func_method_passes(self):
        url = reverse('project-update', kwargs={'pk': self.test_project.id})
        request = self.factory.get(url)
        request.user = self.test_user
        view = ProjectUpdateView()
        view.setup(request, pk=self.test_project.id)

        test_func = view.test_func()
        self.assertEqual(test_func, True)

    def test_test_func_method_fails(self):
        url = reverse('project-update', kwargs={'pk': self.test_project.id})
        request = self.factory.get(url)
        request.user = AnonymousUser
        view = ProjectUpdateView()
        view.setup(request, pk=self.test_project.id)

        test_func = view.test_func()
        self.assertEqual(test_func, False)


class TestProjectCreateView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.test_user = User.objects.create(username='john', email='john@example.com')
        cls.test_user.set_password('mysecret')
        cls.test_user.save()

        cls.test_project = Project.objects.create(title='Portfolio', description='Tasks to complete portfolio website', user=cls.test_user)

    def test_form_valid_method(self):
        url = reverse('project-create')
        request = self.factory.get(url)
        request.user = self.test_user
        data = {
            'title': self.test_project.title,
            'description': self.test_project.description,
        }
        form = ProjectForm(data=data)  
        view = ProjectCreateView()
        view.setup(request)

        form_valid = view.form_valid(form)
        self.assertEqual(form_valid.status_code, 302)


class TestProjectDeleteView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.test_user = User.objects.create(username='john', email='john@example.com')
        cls.test_user.set_password('mysecret')
        cls.test_user.save()

        cls.test_project = Project.objects.create(title='Portfolio', description='Tasks to complete portfolio website', user=cls.test_user)

    def test_test_func_method_passes(self):
        url = reverse('project-delete', kwargs={'pk': self.test_project.id})
        request = self.factory.get(url)
        request.user = self.test_user
        view = ProjectDeleteView()
        view.setup(request, pk=self.test_project.id)

        test_func = view.test_func()
        self.assertEqual(test_func, True)


class TestTaskListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.test_user = User.objects.create(username='john', email='john@example.com')
        cls.test_user.set_password('mysecret')
        cls.test_user.save()

        cls.test_project = Project.objects.create(title='Portfolio', description='Tasks to complete portfolio website', user=cls.test_user)

        # Create 5 Tasks
        number_of_tasks = 5
        for task in range(number_of_tasks):
            Task.objects.create(
                title='Create site map', 
                project_id=cls.test_project.id, 
                priority=3, 
                due_date=datetime.date.today() + datetime.timedelta(days=14), 
                note='Lorem ipsum dolor sit amet.',
                complete=False
            )

    def test_get_queryset_method(self):
        url = reverse('tasks')
        request = self.factory.get(url)
        request.user = self.test_user
        view = TaskListView()
        view.setup(request)

        get_queryset = view.get_queryset()
        filtered_tasks = Task.tasks.filter(project__user = self.test_user)
        self.assertEqual(list(get_queryset), list(filtered_tasks))


class TestCompletedTaskListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.test_user = User.objects.create(username='john', email='john@example.com')
        cls.test_user.set_password('mysecret')
        cls.test_user.save()

        cls.test_project = Project.objects.create(title='Portfolio', description='Tasks to complete portfolio website', user=cls.test_user)

        # Create 5 Tasks
        number_of_tasks = 5
        for task in range(number_of_tasks):
            Task.objects.create(
                title='Create site map', 
                project_id=cls.test_project.id, 
                priority=3, 
                due_date=datetime.date.today() + datetime.timedelta(days=14), 
                note='Lorem ipsum dolor sit amet.',
                complete=True
            )

    def test_get_queryset_method(self):
        url = reverse('completed-tasks')
        request = self.factory.get(url)
        request.user = self.test_user
        view = CompletedTaskListView()
        view.setup(request)

        get_queryset = view.get_queryset()
        filtered_tasks = Task.objects.filter(project__user = self.test_user).filter(complete=True)
        self.assertEqual(list(get_queryset), list(filtered_tasks))


class TestTaskUpdateView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
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

    def test_test_func_method_passes(self):
        url = reverse('task-update', kwargs={'pk': self.test_task.id})
        request = self.factory.get(url)
        request.user = self.test_user
        view = TaskUpdateView()
        view.setup(request, pk=self.test_task.id)

        test_func = view.test_func()
        self.assertEqual(test_func, True)

    def test_test_func_method_fails(self):
        url = reverse('task-update', kwargs={'pk': self.test_task.id})
        request = self.factory.get(url)
        request.user = AnonymousUser
        view = TaskUpdateView()
        view.setup(request, pk=self.test_task.id)

        test_func = view.test_func()
        self.assertEqual(test_func, False)


class TestTaskCreateView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
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

    def test_get_form_kwargs_method(self):
        url = reverse('task-create')
        request = self.factory.get(url)
        request.user = self.test_user
        view = TaskCreateView()
        view.setup(request)

        get_form_kwargs = view.get_form_kwargs()
        self.assertEqual(get_form_kwargs['user'], self.test_user)

    
class TestTaskDeleteView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.c = Client()
        cls.factory = RequestFactory()
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

    def test_get_success_url(self):
        self.c.force_login(self.test_user)
        task = self.test_task
        project_id = task.project_id
        url = reverse_lazy('project-task-list', kwargs={'pk': project_id})
        response = self.c.post(reverse('task-delete', kwargs={'pk': task.id}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(url, f'/project/{project_id}')
        self.assertRedirects(response, url)

    def test_test_func_method_passes(self):
        url = reverse('task-delete', kwargs={'pk': self.test_task.id})
        request = self.factory.get(url)
        request.user = self.test_user
        view = TaskDeleteView()
        view.setup(request, pk=self.test_task.id)

        test_func = view.test_func()
        self.assertEqual(test_func, True)

    def test_test_func_method_fails(self):
        url = reverse('task-delete', kwargs={'pk': self.test_task.id})
        request = self.factory.get(url)
        request.user = AnonymousUser
        view = TaskDeleteView()
        view.setup(request, pk=self.test_task.id)

        test_func = view.test_func()
        self.assertEqual(test_func, False)


class TestUserSignUpView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        # cls.c = Client()
        cls.group = Group.objects.create(name='Task Manager User')

    def test_valid_form_redirects_to_login(self):
        data = {
            'username': 'Sylvie',
            'email': 'sylie@example.com',
            'password1': 'sylpassword',
            'password2': 'sylpassword'
        }
        request = self.factory.post('signup/', data=data) 
        view = UserSignUpView()
        view.setup(request, user_group=self.group)

        post = view.post(request)
        post.client = Client()

        self.assertRedirects(post, '/account/login/', status_code=302)

    def test_nonvalid_form_rerenders(self):
        data = {
            'username': '',
            'email': 'sylie@example.com',
            'password1': 'sylpassword',
            'password2': 'sylpassword'
        }
        request = self.factory.post('signup/', data=data) 
        view = UserSignUpView()
        view.setup(request, user_group=self.group)

        post = view.post(request)
        post.client = Client()

        self.assertEqual(post.status_code, 200)        
