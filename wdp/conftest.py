import pytest
from django.contrib.auth.models import User, Permission


@pytest.fixture
def klient():
    klient = User.objects.create_user(username='Klient', email='em@ail.com', password='ddd')
    return klient

@pytest.fixture
def projektant():
    projektant = User.objects.create_user(username='Projektant', email='em@ail.com', password='ddd')
    permission = Permission.objects.get(codename='add_botsystgenus')
    projektant.user_permissions.add(permission)
    return projektant
