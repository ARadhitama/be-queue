from django.contrib import admin
from django.urls import path, include
from oauth import views

urlpatterns = [
    path('login/', views.login_account, name='login'),
    path('check_login/', views.check_login, name='check'),
    path('signup/', views.signup, name='signup'),
]