from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.urls import reverse

from .forms import *
from .models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.utils import timezone
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


# Create your views here.

def index(request):
    if not request.user.is_authenticated:  # redirect user to login if they are not authenticated
        return redirect('login')
    return redirect('home')


def home(request):
    repeatsCreated = createRepeatingTasks()
    user = request.user
    task_filter = request.GET.get('filter')
    if not user.is_authenticated:   #redirect user to login if they are not authenticated
        return redirect('login')
    
    if task_filter:   
        tasks = get_tasks(user, task_filter)    #Filter tasks if there is a get param
    elif user.is_staff:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(user=user)
    task_model = Task()
    createtask = TaskForm
    edittask = EditTaskForm
    status_choices = task_model._meta.get_field('status').choices

    context = {
        'createform': createtask,
        'editform': edittask,
        'tasks': tasks,
        'choices': status_choices,
        'numOfRepeat': repeatsCreated,
        'filter': task_filter,
    }
    print(task_filter)
    return render(request, 'home.html', context)


def get_tasks(user, tasks_to_get):      # This function filters the tasks
    if tasks_to_get == 'all':
        tasks = Task.objects.all()
    elif tasks_to_get == 'user':
        tasks = Task.objects.filter(user=user)
    elif tasks_to_get == 'unassigned':
        tasks = Task.objects.filter(status=Task.UNASSIGNED)
    elif tasks_to_get == 'completed':
        tasks = Task.objects.filter(status=Task.COMPLETE)
    elif tasks_to_get == 'repeating':
        tasks = Task.objects.filter(repeat=True)
    return tasks


def create_task(request):
    createtaskForm = TaskForm
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('home')


def delete_task(request):
    task_id = request.GET.get('id')
    task = Task.objects.filter(id=task_id)
    task.delete()
    return redirect('home')
    

def createRepeatingTasks():
    repeatCount = 0
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
            new_task.user = User.objects.get(username="carolyn")  # Set the user to Carolyn
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
            new_task.status = 0  # Set the new task status to unassigned
            new_task.save()  # save the new task
            print("Cloning complete")

            # Set the old task repeats to false
            task.repeat = False
            task.save()
            repeatCount += 1
    return repeatCount


def edit_task(request):
    print("edit task")
    if request.method == "POST":
        task = Task.objects.get(id=request.POST.get("id"))
        task.note = request.POST.get("note")
        task.desc = request.POST.get("desc")
        new_user = User.objects.get(id=request.POST.get("user"))
        if (task.user != new_user):
            task.user = new_user
            task.isSeen = False
        task.priority = request.POST.get("priority")
        if (request.POST.get("date_due") != ""):
            task.date_due = request.POST.get("date_due")
        task.repeat = request.POST.get("repeat")
        task.category = Category.objects.get(id=request.POST.get("category"))
        task.interval = request.POST.get("interval")
        task.intervalLength = request.POST.get("intervalLength")
        task.save()
        print("Task was updated successfully")
        return redirect('home')
    else:
        print("Task was not edited. There was an error")
        return redirect('home')


def register(request):
    if not request.user.is_authenticated:  # redirect user to login if they are not authenticated
        return redirect('login')

    User = get_user_model()
    userForm = CreateUserForm

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            print("CREATE USER FORM IS VALID")
            form.save()
            # insert the user into the UserDepartment table
            user = User.objects.get(username=form.cleaned_data['username'])
            userDepartment = UserDepartment()
            userDepartment.user = user
            userDepartment.department = Department.objects.get(id=request.POST.get("department"))
            userDepartment.save()
            print(user.username)
            return redirect(reverse('getAllUsers') + '?status=created&user=' + user.username)
        else:
            print("CREATE USER FORM IS INVALID")
    return redirect('getAllUsers')


def getAllUsers(request):
    if not request.user.is_authenticated:  # redirect user to login if they are not authenticated
        return redirect('login')

    user_list = User.objects.filter(is_active=True)
    userForm = CreateUserForm
    status = request.GET.get('status')
    name = request.GET.get('user')
    context = {
        'user_list': user_list,
        'create_user_form': userForm,
        'status': status,
        'name': name,
    }
    return render(request, 'all_users.html', context)


# when user clicks on the delete button, the user will be removed from the database
def deactivate_user(request, username):
    user = User.objects.get(username=username)
    name = user.first_name
    tasks = Task.objects.filter(user=user)
    for task in tasks:
        task.user = User.objects.get(username='admin')
        task.save()
    user_dept = UserDepartment.objects.get(user=user)
    user_dept.delete()
    user.delete()
    return redirect(reverse('getAllUsers') + '?status=deleted&user=' + name)


def set_as_manager(request, username):
    user = User.objects.get(username=username)
    user.is_staff = True
    user.save()
    return redirect(reverse('getAllUsers') + '?status=managerSet&user=' + user.username)


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
            # check if user is a manager
            if user.is_staff:
                return redirect(reverse('getAllUsers'))
            else:
                # stay on the same page
                return redirect(reverse('user_info', kwargs={'username': user.username}))

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
            if request.user.is_staff:
                return redirect(reverse('getAllUsers') + '?status=reset&user=' + user.username)
            else:
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
        # get the department name from the userdepartment table
        'department': UserDepartment.objects.get(user=user_to_edit).department.name,
    }
    userForm = EditUserForm(initial=initial_values)
    context = {'form': userForm, 'user_to_edit': user_to_edit, 'user': user}
    return render(request, 'viewUserInfo.html', context)
    # return HttpResponseRedirect(reverse('update', args=[current_user.username]), context)


def user_login(request):
    if request.user.is_authenticated:  # redirect user to home if they are authenticated
        return redirect('home')

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
    task = Task.objects.get(id=request.GET.get("taskID"))
    task.status = request.GET.get("newStatusID")
    if task.date_completed is None and task.status is '3':
        task.date_completed = date.today()
    task.save()
    return JsonResponse({'msg': 'Status of this task has been updated'}, status=200)  # Status 200 if successfull.


# Modified this code so that the isSeen html element will show
def mark_as_seen(request):
    task = Task.objects.get(id=request.GET.get("taskID"))
    task_user = task.user.first_name
    msg = "This task has been seen by " + task_user
    if task.isSeen:
        print("Task has already been seen by " + task_user)
        return JsonResponse({"msg": msg}, status=200)
    elif task.user == request.user:
        print("Its you")
        task.isSeen = True
        task.save()
        return JsonResponse({"msg": msg}, status=201)
    else:
        print("Not you at all")
        return JsonResponse({"msg": 'This task has not yet been seen'}, status=204)


#forget password
def ForgetPassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            if not User.objects.filter(username=username).first():
                messages.success(request,'No user found with this username')
                return redirect('forget_password.html')

            user_obj =User.objects.get(username=username)
            token = str(uuid.uuid4())
            profile_obj = Profile.objects.get(user = user_obj)
            profile_obj.forget_password_token = token
            profile.obj.save()
            send_forget_password_mail(user_obj.email, token)
            messages.success(request, 'An email is sent.')
            return redirect('forget_password.html')

    except Exception as e:
        print(e)
    return render(request, 'forget_password.html')