from django.shortcuts import render

from .forms import TaskForm
from .models import *
from django.http import HttpResponse


# Create your views here.
def index(request):
    task = Task.objects.all()
    taskform = TaskForm

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': taskform,
               'task': task}
    return render(request, 'home.html', context)

