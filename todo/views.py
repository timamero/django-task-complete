from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView

from .models import Project, Task
from .forms import TaskForm, ProjectForm


def index(request):
    return render(request, 'index.html')


class ProjectListView(ListView):
    model = Project


def project_task_list(request, pk):
    project = get_object_or_404(Project, id=pk)
    tasks = Task.tasks.filter(project=project)

    context = {
        'project': project,
        'tasks': tasks,
    }
    return render(request, 'todo/project-task-list.html', context=context)


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm


class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy('projects')


class TaskListView(ListView):
    queryset = Task.tasks.all()


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm


class TaskDeleteView(DeleteView):
    model = Task

    def get_success_url(self):
        project_id = Task.tasks.get(pk=self.kwargs['pk']).project_id
        return reverse_lazy('project-task-list', kwargs={'pk': project_id})

class CompletedTaskListView(ListView):
    queryset = Task.objects.filter(complete=True)
    template_name = 'todo/completed-task-list.html'