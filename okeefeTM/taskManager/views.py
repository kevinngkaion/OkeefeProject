from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.urls import reverse

from .forms import *
from .models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages, auth


# Create your views here.

def index(request):
    return redirect('login')


def home(request):
    tasks = Task.objects.all()
    task_model = Task()
    createtask = TaskForm
    edittask = EditTaskForm
    status_choices = task_model._meta.get_field('status').choices

    context = {
        'createform': createtask,
        'editform': edittask,
        'tasks': tasks,
        'choices': status_choices,
    }
    return render(request, 'home.html', context)


def create_task(request):
    createtaskForm = TaskForm
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('home')


def edit_task(request):
    print("edit task")
    if request.method == "POST":
        edittask = Task.objects.get(id=request.POST.get("id"))
        edittask.note = request.POST.get("note")
        edittask.desc = request.POST.get("desc")
        edittask.user = User.objects.get(id=request.POST.get("user"))
        edittask.priority = request.POST.get("priority")
        if (request.POST.get("date_due") != ""):
            edittask.date_due = request.POST.get("date_due")
        edittask.repeat = request.POST.get("repeat")
        edittask.category = Category.objects.get(id=request.POST.get("category"))
        edittask.save()
        print(request.POST)
        return redirect('home')
    else:
        print("No good")
        return redirect('home')

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
    user_to_edit = User.objects.get(username=username)
    user = request.user
    initial_values = {
        'username': user_to_edit.username,
        'first_name': user_to_edit.first_name,
        'last_name': user_to_edit.last_name,
        'email': user_to_edit.email,
    }
    userForm = EditUserForm(initial=initial_values)
    context = {'form': userForm, 'user_to_edit': user_to_edit, 'user': user}
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
    # TODO: Write code to update task status. Request is storing 'taskID' and 'newStatusID' as GET parameters
    # print(request.GET.get("newStatusID"))
    task = Task.objects.get(id=request.GET.get("taskID"))
    task.status = request.GET.get("newStatusID")
    task.save()
    return JsonResponse({'msg': 'Status of this task has been updated'}, status=200)  # Status 200 if successfull.

    
def mark_as_seen(request):
    if User.objects.get(id=request.GET.get("tUID")) == request.user:
        print("Its you")
        seentask = Task.objects.get(id=request.GET.get("taskID"))
        if not seentask.isSeen:
            seentask.isSeen = True
            seentask.save()
        return JsonResponse({"msg": "somejt"}, status=200)
    else:
        print("Not you at all")
        return JsonResponse({"msg": 'not you'}, status=111)
