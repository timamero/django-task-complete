from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('project/<int:pk>', views.project_task_list, name='project-task-list'),
    path('project<int:pk>/update', views.ProjectUpdateView.as_view(), name='project-update'),
    path('project/create', views.ProjectCreateView.as_view(), name='project-create'),
    path('project/<int:pk>/delete', views.ProjectDeleteView.as_view(), name='project-delete'),
    path('task/<int:pk>/update', views.TaskUpdateView.as_view(), name="task-update"),
    path('tasks/', views.TaskListView.as_view(), name='tasks'),
    path('task/create', views.TaskCreateView.as_view(), name="task-create"),
    path('task/<int:pk>/delete', views.TaskDeleteView.as_view(), name='task-delete'),
    path('completedtasks/', views.CompletedTaskListView.as_view(), name='completed-tasks'),
    path('signup/', views.UserSignUpView.as_view(), name='signup')
]
