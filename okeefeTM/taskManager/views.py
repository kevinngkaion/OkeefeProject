from django.shortcuts import render, redirect
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
    return render(request, 'all_users.html', {'list': user_list})


def deactivate_user(request, username):
    user = User.objects.get(username=username)
    user.is_active = False
    user.is_staff = False
    user.save()
    return HttpResponse('User deactivated successfully')


def update_user(request, username):
    user = User.objects.get(User, username=username)

    if request.method == 'POST':
        form = MyUserUpdateForm(request.POST)

        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            return HttpResponse('User Information Updated successfully')
    else:
        form = MyUserUpdateForm(instance=user)

    context = {'form': form, 'user': user}
    return render(request, 'update_user.html', context)


