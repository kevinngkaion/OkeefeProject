from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('register', views.register, name='register'),
  path('allusers', views.getAllUsers, name='getAllUsers'),
  path('deactivate/<str:username>/', views.deactivate_user, name='deactivate_user'),
  path('update/<str:username>/', views.update_user, name='update'),
]
