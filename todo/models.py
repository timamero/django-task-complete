from django.db import models
from django.urls import reverse
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User

class TaskManager(models.Manager):
    def get_queryset(self):
        return super(TaskManager, self).get_queryset().filter(complete=False)


class Project(models.Model):
    """Model representing project which will contain list of tasks"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("project-task-list", args=[str(self.id)])


class Task(models.Model):
    title = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    
    class Priority(models.IntegerChoices):
        LOW = 1
        MEDIUM = 2
        HIGH = 3
    priority = models.IntegerField(choices=Priority.choices, default=Priority.LOW)
    
    due_date = models.DateField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    complete = models.BooleanField(default=False)
    objects = models.Manager()
    tasks = TaskManager()

    class Meta:
            ordering = ['due_date']

    def __str__(self):
            return self.title
        
    def get_absolute_url(self):
        return reverse("project-task-list", args=[str(self.project_id)])
