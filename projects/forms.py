from django import forms
from projects.models import Project, Document


class ProjectModelForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = (
            'title',
            'document',
        )
