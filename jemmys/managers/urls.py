from django.urls import path, include
from .views import dash, Login, Logout

app_name = 'managers'

urlpatterns = [
    path('', dash, name='dashboard'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
]