from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect


def login_view(request):
    """WIDOK LOGOWANIA"""

    if request.method == "GET":
        if request.GET.get('next'):
            return render(request, 'registration/login.html', {'next': request.GET.get('next')})
        else:
            return render(request, 'registration/login.html')

    if request.method == "POST":
        error = []
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if request.POST.get('next'):
                    goto = request.POST.get('next')
                else:
                    goto = '/botanical/'
                return redirect(goto)
            else:
                error.append("Nie znaleziono użytkownika")
                return render(request, 'registration/login.html', {'username': username,
                                                                   'password': password,
                                                                   'error': error})
        else:
            error.append("Nie wypełniono wszystkich pól.")
            return render(request, 'registration/login.html', {'username': username,
                                                               'password': password,
                                                               'error': error})


def logout_view(request):
    """WIDOK WYLOGOWANIA"""
    logout(request)
    return redirect('/')


def signup_view(request):
    """
    WIDOK REJESTRACJI
    Obsługa formularza rejestracji.
        - walidacja danych
        - utworzenie z zapisem nowego użytkownika
        - przydzielenie użytkownika do wybranej grupy uprawnień
        - przekierowanie użytkownika do głównej strony katalogu roślin (/botanical/)
    """
    if request.method == "GET":
        user_groups = Group.objects.all()
        return render(request, 'registration/sign_up.html', {'user_groups': user_groups,
                                                             'user_group': ''})
    if request.method == "POST":
        username = request.POST.get('login')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user_group = request.POST.get('user_group')
        email = request.POST.get('email')
        user_groups = Group.objects.all()
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

        if user_group:
            try:
                group = Group.objects.get(name=user_group)
            except Group.DoesNotExist:
                error.append(f'Grupy użytkowników nie istnieje. {user_group}')
                user_group = None
        else:
            error.append(f'Nie wybrano grupy użytkowników. {user_group}')

        if len(error) == 0:
            user = User.objects.create_user(username, email, password1)
            group.user_set.add(user)
            login(request, user)
            return redirect('/botanical/')
        else:
            return render(request, 'registration/sign_up.html', {'username': username,
                                                                 'email': email,
                                                                 'user_groups': user_groups,
                                                                 'user_group': user_group,
                                                                 'error': error})
