from django.contrib import admin
from django.urls import path
from .views import index, signup_view, logout_view, login_view

urlpatterns = [
    path('', index, name="home"),
    path('signup/', signup_view, name="signup"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
]
