from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda request: redirect('chat')),  # redirige /ia/ → /ia/chat/
    path('chat/', views.chat_view, name='chat'),
]
