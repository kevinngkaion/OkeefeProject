from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
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
                if remember_me is not None:
                    request.session.set_expired(0)

                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

class UpdatedLoginView(LoginView):
    form_class = LoginForm
    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']
        if not remember_me:
            self.request.session.set_expiry(0)
            self.requset.session.modified = True
        return super(UpdatedLoginView, self).form_valid(form)

def user_logout(request):
    logout(request)
    return redirect('login')

def update_task_status(request):
    # TODO: Write code to update task status. Request is storing 'taskID' and 'newStatus' as GET parameters

    return JsonResponse({'msg': 'Status of this task has been updated'}, status=200) # Status 200 if successfull.