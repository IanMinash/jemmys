from django.urls import path, include
from .views import dash

urlpatterns = [
    path('', dash, name='dashboard'),
]