from django.contrib import admin

from .models import Project, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'complete')
    list_filter = ('complete',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'description')
    list_filter = ('user',)
