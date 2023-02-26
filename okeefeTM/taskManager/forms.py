from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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


# class UserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username',
#                   'first_name',
#                   'last_name',
#                   'email',
#                   'password',
#                   'groups',
#                   'is_staff',
#                   'is_active',
#                   'is_superuser',
#                   'last_login',
#                   'date_joined'
#                   ]

class CreateUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)
