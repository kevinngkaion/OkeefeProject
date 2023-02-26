from django.urls import path, include
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('accounts/login/', views.login, name='login'),
  path('',include('django.contrib.auth.urls'))
  #path('account/profile/', home)
]