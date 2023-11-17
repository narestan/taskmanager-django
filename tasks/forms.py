from django import forms
from tasks.models import Task, Agent, Category, FollowUp
from projects.models import Project


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

    # def clean_first_name(self):
    #     data = self.cleaned_data["first_name"]
    #     # if data != "Joe":
    #     #     raise ValidationError("Your name is not Joe")
    #     return data

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
        }


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            'name',
        )


class FollowUpModelForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = (
            'notes',
            'file'
        )
