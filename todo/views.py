from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView

from .models import Project, Task


def index(request):
    return render(request, 'index.html')


class ProjectListView(ListView):
    model = Project


def project_task_list(request, pk):
    project = get_object_or_404(Project, id=pk)
    tasks = Task.objects.filter(project=project)
    # tags = tasks.tag.all()

    context = {
        'project': project,
        'tasks': tasks,
        # 'tags': tags,
    }
    return render(request, 'todo/project-task-list.html', context=context)