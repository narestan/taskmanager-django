from django import forms
from tasks.models import Task


class TaskModelForm(forms.ModelForm):
    class Meta:
        model = Task
        field = '__all__'
        exclude = ['created_at']
