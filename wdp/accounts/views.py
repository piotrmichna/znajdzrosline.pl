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


def signup_view(request):
    if request.method == "GET":
        return render(request, 'registration/sign_up.html')
    if request.method == "POST":
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        error = []
        if not email:
            error.append('Adres e-mail jest wymagany.')
        else:
            if '@' not in email:
                error.append('Adres e-mail jest nie poprawny.')
            else:
                if User.objects.filter(email=email).count():
                    error.append('Konto na podany adres e-mail zostało już utworzone.')

        if len(username) < 5:
            error.append('Brak nazwy użytkownika lub jest za krótka.')
        else:
            if User.objects.filter(username=username).count():
                error.append('Użytkownik o takiej nazwie już istnieje.')

        if len(password1) < 8:
            error.append('Hasło jest krótsze niż 8 znaków')
        else:
            if password2 != password1:
                error.append('Podane hasła są niezgodne.')

        if len(error) == 0:
            user = User.objects.create_user(username, email, password1)
            login(request, user)
            return redirect('/botanical/')
        else:
            return render(request, 'registration/sign_up.html', {'username': username,
                                                                 'email': email,
                                                                 'error': error})
