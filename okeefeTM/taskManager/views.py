
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.conf import settings
from .forms import *
from .models import *
from django.http import JsonResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail


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

    # Get all tasks and set status to not started if there is a user assigned and status is unassigned
    tasks = Task.objects.filter(status=Task.UNASSIGNED).exclude(user=User.objects.get(username="admin"))
    for task in tasks:
        task.status = Task.NOT_STARTED
        task.save()
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
            user = User.objects.get(id=request.POST.get("user"))
            form.save()
            #should only send task creation mail if user assigned is Unassigned(admin)
            if user is not User.objects.get(username="admin"):
                try:
                    send_mail("A Task has been assigned to you",
                        "Task Name: " + request.POST.get("name") + "\n" +
                        "Description: " + request.POST.get("desc") + "\n" +
                        "For more details please visit http://www.okeefetm.ca/",
                        settings.EMAIL_HOST_USER,
                        [user.username])
                except:
                    print("There was an error sending mail for creating a task")
    
    
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
            # Only send mail if new_user is not Unassigned (admin)
            if new_user is not User.objects.get(username="admin"):
                try:
                    send_mail("A Task has been reassigned to you",
                            "Task Name: " + task.name + "\n" +
                            "Description: " + task.desc + "\n" +
                            "For more details please visit http://www.okeefetm.ca/",
                            settings.EMAIL_HOST_USER,
                            [task.user.username])
                except:
                    print("There was an error sending an email for reassigning a task user")
            task.isSeen = False
        task.priority = request.POST.get("priority")
        if (request.POST.get("date_due") != ""):
            task.date_due = request.POST.get("date_due")
        task.repeat = request.POST.get("repeat")
        print(task.repeat)
        if task.repeat is "True":
            print("In true condition")
            task.interval = request.POST.get("interval")
            task.intervalLength = request.POST.get("intervalLength")
        else:
            task.interval = ''
            task.intervalLength = None
        
        task.category = Category.objects.get(id=request.POST.get("category"))

        # Send email if new status is "Complete"
        new_status = request.POST.get('status')
        if (task.status != new_status and new_status == 3):
            try:
                send_mail(
                    "A task has been completed",
                    "Task Name: " + task.name + "\n" +
                    "Description: " + task.desc + "\n" +
                    "For more details please visit http://www.okeefetm.ca/",
                    settings.EMAIL_HOST_USER,
                    ['arresteddevelopers2023@gmail.com']
                )
            except:
                print("There was an error sending an email for the completion of a task in editing task")
            task.status = new_status
        print(task.intervalLength)
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
            # save the username of the user (which should be their email) into the user.email field
            user.email = user.username
            user.save()
            print(user.username)
            try:
                send_mail("O'Keefe Ranch Task Manager: Your Account Has Been Created",
                        "Your account for the O'Keefe Task Manager has been created\nIf you do not know your password, please see your manager or Ranch Curator\n",
                        settings.EMAIL_HOST_USER,
                        [user.email])
            except:
                print("There was an error sending an email for creating a user")
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
    if user.is_staff:
        status = "managerRemoved"
    else:
        status = "managerSet"
    user.is_staff = not user.is_staff
    user.save()
    return redirect(reverse('getAllUsers') + '?status=' + status + '&user=' + user.username)


def update_user(request, username):
    user = User.objects.get(username=username)
    userForm = MyUserUpdateForm(instance=user)
    if request.method == 'POST':
        form = MyUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
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
    status = 'pending'
    if request.method == 'POST':
        form = MyResetPasswordForm(request.POST, instance=user)
        if form.is_valid():
            user.set_password(form.cleaned_data['password1'])
            user.save()
            if request.user.is_staff:
                return redirect(reverse('getAllUsers') + '?status=reset&user=' + user.username)
            else:
                return redirect('login')
        else:
            status = 'failed'
    context = {'form': userForm, 'user': user, 'status': status}
    return render(request, 'reset_password.html', context)


def getUserInfo(request, username):
    user_to_edit = User.objects.get(username=username)
    user = request.user
    # get the department name from the userdepartment table
    department = UserDepartment.objects.get(user=user_to_edit).department.name
    initial_values = {
        'username': user_to_edit.username,
        'first_name': user_to_edit.first_name,
        'last_name': user_to_edit.last_name,
        'email': user_to_edit.email,
        'department': Department.objects.get(name=department),
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
    if task.date_completed is None and task.status == '3':
        task.date_completed = date.today()
        try:
            send_mail(
            "A task has been completed",
            "Task Name: " + task.name + "\n" +
            "Description: " + task.desc + "\n" +
            "For more details please visit http://www.okeefetm.ca/",
            settings.EMAIL_HOST_USER,
            ['arresteddevelopers2023@gmail.com']
            )
        except:
            print("There was an error sending the email for completing a task without editing the task")
    task.save()
    #print("After task got saved")
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


# forget password
User = get_user_model()


def forgetpassword(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # User does not exist, show error message
            return render(request, 'forget_password.html', {'error': 'User does not exist'})

        if user.is_staff:
            # User is staff, send reset password email
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_link = request.build_absolute_uri(reverse('change_password', kwargs={'uidb64': uidb64, 'token': token}))
            try:
                send_mail(
                    'Reset your password',
                    f'Click the following link to reset your password: {reset_link}',
                    'noreply@gmail.com',
                    [user.email],
                    fail_silently=False,
                )
            except:
                print("There was an error sending mail for password reset")

            # Show success message
            return render(request, 'forget_password.html', {'success': 'Password reset link has been sent to your email.'})
        else:
            # User is not staff, show error message
            return render(request, 'forget_password.html', {'error': 'Please contact your manager to reset the password.'})
    else:
        return render(request, 'forget_password.html')

def change_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and PasswordResetTokenGenerator().check_token(user, token):
        if request.method == 'POST':
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1 != password2:
                return render(request, 'change_password.html', {'error': 'Passwords do not match'})
            elif len(password1) < 8:
                return render(request, 'change_password.html', {'error': 'Password must be at least 8 characters long'})
            else:
                user.set_password(password1)
                user.save()
                return render(request, 'change_password.html', {'success': 'Password reset successful.'})
            return redirect(reverse_lazy('login'))
        return render(request, 'change_password.html', {'user': user})
    else:
        messages.error(request, 'Invalid password reset link')
        return redirect(reverse_lazy('login'))