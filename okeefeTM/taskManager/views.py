from audioop import reverse

from django.shortcuts import render
from django.contrib.auth import get_user_model, login
from .forms import *
from .models import *
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from taskManager.models import Task


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


def register(request):
    User = get_user_model()
    userForm = CreateUserForm

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponse('success')
    context = {'form': userForm}
    return render(request, 'sample.html', context)
