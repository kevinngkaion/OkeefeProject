from django.shortcuts import render
from django.contrib.auth import get_user_model
from .forms import *
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from taskManager.models import Task
from django.contrib.auth.models import User


# Create your views here.

def index(request):
    tasks = Task.objects.all()
    
    taskform = TaskForm

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': taskform, 'tasks': tasks}
    return render(request, 'home.html', context)


def register(request):
    User = get_user_model()
    userForm = CreateUserForm

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Create User Successfully!')
    context = {'form': userForm}
    return render(request, 'sample.html', context)

def getAllUsers(request):
    user_list = User.objects.all()
    return render(request, 'allusers.html', {'list': user_list})

