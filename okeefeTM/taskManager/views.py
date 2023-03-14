from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from .forms import *
from .models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from taskManager.models import Task
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.utils import timezone
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


# Create your views here.

def index(request):
    return redirect('login')


def home(request):
    createRepeatingTasks()
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

def createRepeatingTasks():
    repeatingTasks = Task.objects.filter(repeat=True).exclude(date_completed=None)
    for task in repeatingTasks:
        interval = task.interval
        length = task.intervalLength
        if interval == "Daily":
            nextDate = task.date_completed + timedelta(days=length)
            print("The date that this task will be created again is")
            print(nextDate)
        elif interval == "Weekly":
            nextDate = task.date_completed + timedelta(weeks=length)
        elif interval == "Monthly":
            nextDate = task.date_completed + relativedelta(months=length)
        elif interval == "Yearly":
            nextDate = task.date_compelted + relativedelta(years=length)

        # Check if nextDate is today
        if nextDate == date.today():
            # Clone that task into the task model as a new task
            print("Cloning Task")
            new_task = Task()
            new_task.id = None
            new_task.name = task.name
            new_task.user = User.objects.get(username="carolyn") #Set the user to Carolyn
            new_task.category = task.category
            new_task.priority = task.priority
            new_task.date_due = None
            new_task.repeat = task.repeat
            new_task.interval = task.interval
            new_task.intervalLength = task.intervalLength
            new_task.note = None
            new_task.desc = task.desc
            new_task.date_created = date.today()
            new_task.date_completed = None
            new_task.status = 0 #Set the new task status to unassigned
            new_task.save() #save the new task
            print("Cloning complete")

            # Set the old task repeats to false
            task.repeat = False
            task.save()
    return

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
    user = User.objects.get(username=username)
    userForm = MyUserUpdateForm

    if request.method == 'POST':
        form = MyUserUpdateForm(request.POST)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            # form.save()
            user.save()
            return HttpResponse('User Information Updated successfully')
    # else:
    #     form = MyUserUpdateForm(instance=user)

    context = {'form': userForm, 'user': user}
    return render(request, 'update_user.html', context)


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

    return JsonResponse({'msg': 'Status of this task has been updated'}, status=200) # Status 200 if successfull.