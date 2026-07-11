from .views import chat_gateway
from django.urls import path

urlpatterns = [
    path('chat/', chat_gateway)
]