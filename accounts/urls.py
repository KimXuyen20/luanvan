from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('',  views.home, name="home"),
    path('accounts/register/',  views.register, name = "register"),
    path('accounts/login/',  views.login, name = "login"),
    path('accounts/logout/',  views.logoutPage, name = "logout"),
    path('accounts/dashboard/',  views.dashboard, name = "dashboard"),
    path('accounts/edit/',  views.edit, name = "edit"),
]