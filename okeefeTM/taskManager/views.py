from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def index(request):
  return render(request, 'navbar.html')

def home(request):
  return render(request,'home.html')

def login_user(request):
  return render(request, 'authenticate/login.html', {})