from django import forms
from tasks.models import Task, Agent, Category, FollowUp
from projects.models import Project
from django_jalali.forms import jDateTimeField
from django_jalali.admin.widgets import AdminSplitjDateTime


class TaskModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            'task_name',
            'info',
            'agent',
            'date_start',
            'date_end',
            'category',
            'project',

        )
        labels = {
            'task_name': 'نام کار',
            'info': 'توضیحات',
            'agent': 'کاربر',
            'date_start': 'تاریخ شروع',
            'date_end': 'تاریخ پایان',
            'category': 'دسته‌بندی',
            'project': 'شماره ثبت سفارش',
        }
        widgets = {
            'date_start': AdminSplitjDateTime(),
            'date_end': AdminSplitjDateTime(),
            # Add other widgets if necessary
        }

    def clean(self):
        pass


class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        agents = Agent.objects.filter(organisation=request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents


class TaskCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            'category',
        )
        labels = {
            'project': 'Project Name',
            'category': 'وضعیت',
        }


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            'name',
        )
        labels = {
            'name': 'نام',
        }


class FollowUpModelForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = (
            'notes',
            'file'
        )
        labels = {
            'notes': 'یادداشت‌ها',
            'file': 'فایل',
        }


# search form
class ProjectSearchForm(forms.Form):
    project_id = forms.IntegerField(label='Project ID')
