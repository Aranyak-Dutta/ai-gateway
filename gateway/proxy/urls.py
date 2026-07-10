from .views import call_it
from django.urls import path

urlpatterns = [
    path('chat/', call_it)
]