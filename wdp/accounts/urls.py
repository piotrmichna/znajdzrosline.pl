from django.contrib import admin
from django.urls import path
from .views import index, sign_up, logout_view, login_view

urlpatterns = [
    path('', index, name="home"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
]
