from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password


User = get_user_model()


class AgentModelForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'position',
            'mobile_number',
        )
        labels = {
            'position': 'سمت',
            'mobile_number': 'شماره همراه',
        }

    def save(self, commit=True):
        user = super(AgentModelForm, self).save(commit=False)
        password = self.cleaned_data["password"]
        user.password = make_password(password)
        if commit:
            user.save()
        return user
