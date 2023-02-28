from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('register', views.register, name='register'),
  path('allusers', views.getAllUsers, name='getAllUsers'),
  path('delete_user', views.delete_user, name='deleteUser')
]
