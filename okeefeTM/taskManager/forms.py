from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.forms import ModelForm, widgets
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

class EditTaskForm(ModelForm):
    id = forms.IntegerField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        self.fields['status'].widget.attrs['class'] = 'form-select'
        self.fields['note'].widget = widgets.Textarea(
            attrs={'class': 'form-control', 'rows': '3'}
        )
    class Meta:
        model = Task
        labels = {
            'status': 'Status',
            'user': 'Assign To',
            'desc': 'Description',
            'date_due': 'Date Due',
            'repeat': 'Is this a recurring task?',
            'note': 'Notes'
            }
        fields = [
            'id',
            'status',
            'user',
            'category',
            'priority',
            'date_due',
            'repeat',
            'desc',
            'note',
            ]

            
class CreateUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')


class EditUserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget = widgets.TextInput(attrs={'class': 'form-control', 'disabled': True})
        self.fields['first_name'].widget = widgets.TextInput(attrs={'class': 'form-control', 'disabled': True})
        self.fields['last_name'].widget = widgets.TextInput(attrs={'class': 'form-control', 'disabled': True})
        self.fields['email'].widget = widgets.EmailInput(attrs={'class': 'form-control', 'disabled': True})

    class Meta:
        model = User
        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
        }
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]


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
        fields = ['first_name', 'last_name', 'email']


class MyResetPasswordForm(forms.ModelForm):
    password1 = forms.CharField(label='New password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm new password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two passwords do not match")
        return cleaned_data
