from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

urlpatterns = [
  path('', views.index, name='index'),
  path('accounts/login/', views.login, name='login'),
]