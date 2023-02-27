from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.forms import ModelForm
from .models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name',
                  'user',
                  'category',
                  'priority',
                  'date_due',
                  'repeat',
                  'desc'
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