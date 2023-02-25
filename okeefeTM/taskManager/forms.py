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
