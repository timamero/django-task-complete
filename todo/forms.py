from django import forms
from django.forms import widgets

from .models import Project, Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'project', 'priority', 'due_date', 'note', 'tag']
        widgets = {
            'due_date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'note': forms.Textarea(attrs={'rows':2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'input'})
        self.fields['due_date'].widget.attrs.update({'class': 'input'})
        self.fields['note'].widget.attrs.update({'class': 'textarea'})
        self.fields['tag'].widget.attrs.update({'class': 'multiple'})

    
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows':2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'input'})
        self.fields['description'].widget.attrs.update({'class': 'textarea'})
