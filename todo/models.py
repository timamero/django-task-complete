from django.db import models
from django.db.models.deletion import CASCADE

class Project(models.Model):
    """Model representing project which will contain list of tasks"""
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title

class Tag(models.Model):
    """Model representing tag"""
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


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
   tag = models.ManyToManyField(Tag)
   complete = models.BooleanField(default=False)

   class Meta:
        ordering = ['due_date']

   def __str__(self):
        return self.title
