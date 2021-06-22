from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, UpdateView, DeleteView, CreateView

from .models import Project, Task
from .forms import TaskForm, ProjectForm


def index(request):
    return render(request, 'index.html')


class ProjectListView(LoginRequiredMixin, ListView):
    login_url = '/account/login/'
    model = Project

    # List only projects that belong to logged in user
    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


@login_required
def project_task_list(request, pk):
    project = get_object_or_404(Project, id=pk)
    tasks = Task.tasks.filter(project=project)

    if request.user != project.user:
        return redirect('/account/login/?next=%s')

    context = {
        'project': project,
        'tasks': tasks,
    }
    return render(request, 'todo/project-task-list.html', context=context)


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = '/account/login/'
    model = Project
    form_class = ProjectForm

    def test_func(self):
        project = self.get_object()
        return self.request.user == project.user
    

class ProjectCreateView(LoginRequiredMixin, CreateView):
    login_url = '/account/login/'
    model = Project
    form_class = ProjectForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = '/account/login/'
    model = Project
    success_url = reverse_lazy('projects')

    def test_func(self):
        project = self.get_object()
        return self.request.user == project.user


class TaskListView(LoginRequiredMixin, ListView):
    login_url = '/account/login/'
    
    def get_queryset(self):
        return Task.tasks.filter(project__user = self.request.user)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = '/account/login/'
    model = Task
    form_class = TaskForm

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.project.user


class TaskCreateView(LoginRequiredMixin, CreateView):
    login_url = '/account/login/'
    model = Task
    form_class = TaskForm
    
    def get_form_kwargs(self):
        kwargs = super(TaskCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/account/login/'
    model = Task

    def get_success_url(self):
        project_id = Task.tasks.get(pk=self.kwargs['pk']).project_id
        return reverse_lazy('project-task-list', kwargs={'pk': project_id})

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.project.user


class CompletedTaskListView(LoginRequiredMixin, ListView):
    login_url = '/account/login/'
    template_name = 'todo/completed-task-list.html'

    def get_queryset(self):
        return Task.objects.filter(project__user = self.request.user).filter(complete=True)


class PasswordReset(LoginRequiredMixin, PasswordResetView):
    login_url = '/account/login/'
    from_email = 'timadevtest@gmail.com'
    subject_template_name = 'Task Complete: Password reset link'
