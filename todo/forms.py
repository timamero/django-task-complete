from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Project, Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'project', 'priority', 'due_date', 'note', 'complete']
        labels = {
            'complete': 'Task Completed?'
        }
        widgets = {
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'note': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, request=None, **kwargs):
        user = kwargs.pop('user')
        super(TaskForm, self).__init__(*args, **kwargs)
        
        self.request = request
        if request is not None:
            current_project = request

        self.fields['title'].widget.attrs.update({'class': 'input'})
        self.fields['due_date'].widget.attrs.update({'class': 'input'})
        self.fields['note'].widget.attrs.update({'class': 'textarea'})
        self.fields['project'].queryset = Project.objects.filter(user=user)
        if current_project:
            self.fields['project'].initial = current_project

        # https://stackoverflow.com/questions/24041649/filtering-a-model-in-a-createview-with-get-queryset


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'input'})
        self.fields['description'].widget.attrs.update({'class': 'textarea'})


class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(required="true")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
