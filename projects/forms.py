from django import forms
from projects.models import Project, Document


class ProjectModelForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        labels = {
            'name': 'نام کالا',
            'proforma_num_reg': 'شماره ثبت پروفرما',
            'proforma_name': 'شماره پروفرما',
            'price': 'مبلغ',
            'weight': 'وزن',
            'currency': 'واحد ارز'
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = (
            'title',
            'document',
        )
        labels = {
            'title': 'عنوان',
            'document': 'سند'
        }
