from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def index(request):
    return render(request, 'index.html')


def login_view(request):
    if request.method == "GET":
        return render(request, 'registration/login.html')

    if request.method == "POST":
        error = []
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/botanical/')
            else:
                error.append("Nie znaleziono urzytkownika")
                return render(request, 'registration/login.html', {'username': username,
                                                                   'password': password,
                                                                   'error': error})
        else:
            error.append("Nie wypełniono wszystkich pól.")
            return render(request, 'registration/login.html', {'username': username,
                                                               'password': password,
                                                               'error': error})


def logout_view(request):
    logout(request)
    return redirect('/')
