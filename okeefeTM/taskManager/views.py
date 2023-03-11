from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.urls import reverse

from .forms import *
from .models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from taskManager.models import Task
from django.contrib.auth.models import User
from django.contrib import messages, auth


# Create your views here.

def index(request):
    return redirect('login')


def home(request):
    tasks = Task.objects.all()
    taskform = TaskForm
    task_model = Task()
    status_choices = task_model._meta.get_field('status').choices

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
    context = {
        'form': taskform,
        'tasks': tasks,
        'choices': status_choices,
    }
    return render(request, 'home.html', context)


def register(request):
    User = get_user_model()
    userForm = CreateUserForm

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            # return HttpResponse('Create User Successfully!')
            return redirect(reverse('getAllUsers'))
    context = {'create_user_form': userForm}
    # return render(request, 'sample.html', context)
    return render(request, 'sample.html', context)


def getAllUsers(request):
    user_list = User.objects.filter(is_active=True)
    userForm = CreateUserForm
    return render(request, 'all_users.html', {'user_list': user_list, 'create_user_form': userForm})


def deactivate_user(request, username):
    user = User.objects.get(username=username)
    user.is_active = False
    user.is_staff = False
    user.save()
    return redirect(reverse('getAllUsers'))


def set_as_manager(request, username):
    user = User.objects.get(username=username)
    user.is_staff = True
    user.save()
    return redirect(reverse('getAllUsers'))

def update_user(request, username):
    user = User.objects.get(username=username)
    userForm = MyUserUpdateForm(instance=user)
    if request.method == 'POST':
        form = MyUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            return redirect(reverse('getAllUsers'))
    context = {'form': userForm, 'user': user}
    return render(request, 'all_users.html', context)


def reset_password(request, username):
    user = User.objects.get(username=username)
    userForm = MyResetPasswordForm(instance=user)
    if request.method == 'POST':
        form = MyResetPasswordForm(request.POST, instance=user)
        if form.is_valid():
            # user.password = form.cleaned_data['password1']
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('login')
    context = {'form': userForm, 'user': user}
    return render(request, 'reset_password.html', context)


def getUserInfo(request, username):
    user = User.objects.get(username=username)
    current_user = request.user
    initial_values = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }
    userForm = EditUserForm(initial=initial_values)
    context = {'form': userForm, 'user': user, 'current_user': current_user}
    return render(request, 'viewUserInfo.html', context)
    # return HttpResponseRedirect(reverse('update', args=[current_user.username]), context)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def update_task_status(request):
    # TODO: Write code to update task status. Request is storing 'taskID' and 'newStatus' as GET parameters

    return JsonResponse({'msg': 'Status of this task has been updated'}, status=200)  # Status 200 if successfull.
