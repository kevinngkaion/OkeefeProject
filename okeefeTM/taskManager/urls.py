from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

urlpatterns = [
  path('', views.index, name='index'),
  path('register', views.register, name='register'),
  path('allusers', views.getAllUsers, name='getAllUsers'),
  path('deactivate/<str:username>/', views.deactivate_user, name='deactivate_user'),
  path('update/<str:username>/', views.update_user, name='update'),
  path('login/', views.user_login, name='login'),
  path('logout/', views.user_logout, name='logout'),
  path('home', views.home, name='home'),
  path('update_task_status', views.update_task_status, name='update_task_status'),
  path('edit_task', views.edit_task, name='edit_task'),
  path('create_task', views.create_task, name='create_task'),
  path('mark_as_seen', views.mark_as_seen, name='mark_as_seen')
]


