
from django.urls import path

from authors.views import login_create, login_view, logout_view, register_view

app_name = 'authors'

urlpatterns = [
    path('register/', register_view, name='register_create'),
    path('login/', login_view, name='login'),
    path('login/create/', login_create, name='login_create'),
    path('logout/', logout_view, name='logout'),


]
