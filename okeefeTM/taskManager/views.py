from django.shortcuts import render
from django.contrib.auth import get_user_model
from .forms import *
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from taskManager.models import Task
from django.contrib.auth.models import User

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


def delete_user(request, username):
    user_to_delete = User.objects.get(username=username)
    user_to_delete.delete()
    return HttpResponse('Delete User Successfully!')
