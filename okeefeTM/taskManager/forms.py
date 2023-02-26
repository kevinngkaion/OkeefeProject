from django.contrib.auth.forms import UserCreationForm
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
