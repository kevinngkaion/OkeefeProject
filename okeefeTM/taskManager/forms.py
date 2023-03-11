from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.forms import ModelForm, widgets
from .models import Task
from django import forms
from django.contrib.auth.models import User


class TaskForm(ModelForm):    
    # This is for the styling of the form fields
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
        self.fields['repeat'].widget.attrs['id'] = 'id_repeat_create'
        self.fields['desc'].widget = widgets.Textarea(
            attrs={'class': 'form-control', 'rows': '5'}
        )
        self.fields['interval'].widget.attrs['class'] = 'form-select'
        self.fields['interval'].widget.attrs['id'] = 'id_interval_create'
        self.fields['interval'].widget.attrs['disabled'] = True
        self.fields['intervalLength'].widget.attrs['placeholder'] = 'Frequency'
        self.fields['intervalLength'].widget.attrs['class'] = 'form-control'
        self.fields['intervalLength'].widget.attrs['id'] = 'id_intervalLength_create'
        self.fields['intervalLength'].widget.attrs['disabled'] = True
        


    class Meta:
        model = Task
        labels = {
            'name': 'Task Name',
            'user': 'Assign To',
            'desc': 'Description',
            'date_due': 'Date Due',
            'repeat': 'Is this a recurring task?',
            'intervalLength': 'Length',
            }
        fields = [
            'name',
            'user',
            'category',
            'priority',
            'date_due',
            'repeat',
            'intervalLength',
            'interval',
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
                raise forms.ValidationError(
                    "Invalid email or password. Please try again."
                )
            elif not user.is_active:
                raise forms.ValidationError("This account is inactive.")
        return self.cleaned_data


class MyUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
