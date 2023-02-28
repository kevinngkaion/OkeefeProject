from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

urlpatterns = [
  path('', views.index, name='index'),
  path('login/', views.user_login, name='login'),
  path('logintest/', views.login_test, name='test'),
  path('logout/', views.user_logout, name='logout'),
  path('home', views.home, name='home'),
]