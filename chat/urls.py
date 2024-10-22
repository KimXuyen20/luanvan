from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('chat/chat/',  views.chat, name = "chat"),
]