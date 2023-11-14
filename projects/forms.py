from django import forms
from projects.models import Project


class ProjectModelForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            'name',
            'floor_number',
            'apartment_number',
            'address',
        )
