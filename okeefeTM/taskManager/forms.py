from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.forms import ModelForm, widgets, ValidationError
from .models import Task
from django import forms
from django.contrib.auth.models import User


class TaskForm(ModelForm):    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['user'].widget.attrs['class'] = 'form-select'
        self.fields['category'].widget.attrs['class'] = 'form-select'
        self.fields['priority'].widget.attrs['class'] = 'form-select'
        self.fields['date_due'].widget = widgets.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}
        )
        self.fields['repeat'].widget.attrs['class'] = 'form-select'
        self.fields['desc'].widget = widgets.Textarea(
            attrs={'class': 'form-control', 'rows': '5'}
        )

    class Meta:
        model = Task
        labels = {
            'name': 'Task Name',
            'user': 'Assign To',
            'desc': 'Description',
            'date_due': 'Date Due',
            'repeat': 'Is this a recurring task?'
            }
        fields = [
            'name',
            'user',
            'category',
            'priority',
            'date_due',
            'repeat',
            'desc',
            ]


class CreateUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email", "first_name", "last_name")


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="email",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        label="password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)

            if user is None:
                raise ValidationError(
                    "Invalid email or password. Please try again."
                )

        return self.cleaned_data


class MyUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']



