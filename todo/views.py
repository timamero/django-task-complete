from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, UpdateView, DeleteView, CreateView

from .models import Project, Task
from .forms import TaskForm, ProjectForm


def index(request):
    return render(request, 'index.html')


class ProjectListView(LoginRequiredMixin, ListView):
    login_url = '/account/login/'
    model = Project

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


@login_required
def project_task_list(request, pk):
    project = get_object_or_404(Project, id=pk)
    tasks = Task.tasks.filter(project=project)

    context = {
        'project': project,
        'tasks': tasks,
    }
    return render(request, 'todo/project-task-list.html', context=context)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('projects')


class TaskListView(LoginRequiredMixin, ListView):
    queryset = Task.tasks.all()


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task

    def get_success_url(self):
        project_id = Task.tasks.get(pk=self.kwargs['pk']).project_id
        return reverse_lazy('project-task-list', kwargs={'pk': project_id})


class CompletedTaskListView(LoginRequiredMixin, ListView):
    queryset = Task.objects.filter(complete=True)
    template_name = 'todo/completed-task-list.html'