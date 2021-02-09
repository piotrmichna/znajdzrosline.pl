import pytest
from django.contrib.auth.models import User, Permission
from django.test import TestCase, Client
from django.urls import reverse
import conftest
from botanical.models import BotSystGenus, BotSystSpecies, BotSystCultivar, PlantBodyType, PlantDescriptions, \
    PlntLibraries


@pytest.mark.django_db
def test_post_no_authorized_genus_view(client):
    User.objects.create_user('test2')

    client.force_login('test2')
    response = client.post('/botanical/add/genus/', {'lac_name': 'Fraxinus', 'pl_name': 'jesion'})
    assert response.status_code == 403

# @pytest.mark.django_db
# def test_post_authorized_genus_view(client):
#     user = User.objects.create_user(username='test', password='TestPass')
#     permission = Permission.objects.get(codename='add_botsystgenus')
#     user.user_permissions.add(permission)
#     user.save()
#
#     client.login(username='test', password='TestPass')
#     response = client.post('/botanical/add/genus/', {'lac_name': 'Fraxinus', 'pl_name': 'jesion'})
#
#     assert BotSystGenus.objects.get(lac_name='Fraxinus')
#
#
# @pytest.mark.django_db
# def test_post_authorized_species_view(client):
#     """TEST DODAWANIA NAZW GATUNKÓW"""
#     user = User.objects.create_user(username='test', password='TestPass')
#     permission = Permission.objects.get(codename='add_botsystgenus')
#     user.user_permissions.add(permission)
#     user.save()
#
#     client.login(username='test', password='TestPass')
#     response = client.post('/botanical/add/species/', {'lac_name': 'excelsrior', 'pl_name': 'wyniosły'})
#
#     assert BotSystGenus.objects.get(lac_name='excelsrior')
#
#
# @pytest.mark.django_db
# def test_authorized_botanical_add_type_view(client):
#     """
#     Test BotanicalAddTypeView
#
#     - sprawdzenie poprawności dodawania unikalnych nazw typów rośliny
#     _ sprawdzenie zwracania komunikatu error po ponownym dodaniu tej samej rośliny
#     """
#     user = User.objects.create_user(username='test', password='TestPass')
#     permission = Permission.objects.get(codename='add_botsystgenus')
#     user.user_permissions.add(permission)
#     user.save()
#     client.login(username='test', password='TestPass')
#
#     response = client.post('/botanical/add/type/', {'body_type': 'Rośliny zielne'})
#     assert PlantBodyType.objects.get(body_type='Rośliny zielne')
#
#     response = client.post('/botanical/add/type/', {'body_type': 'Rośliny zielne'})
#     assert len(response.error) > 0
#
#
# @pytest.mark.django_db
# def test_authorized_botanical_syst_add_view(client):
#     """
#     Test BotanicalSystAddView
#
#     sprawdzenie zmiennej sesyjnej ustawianej po wyborze gatunku
#     """
#     user = User.objects.create_user(username='test', password='TestPass')
#     permission = Permission.objects.get(codename='add_botsystgenus')
#     user.user_permissions.add(permission)
#     user.save()
#
#     client.login(username='test', password='TestPass')
#     response = client.post('/botanical/add/', {'genus_name': 'Acer'})
#     assert 'Acer' == response.session.get('genus_name')
#
#     response = client.post('/botanical/add/', {'species_name': 'platanus'})
#     assert 'platanus' == response.session.get('species_name')
#
#     response = client.post('/botanical/add/', {'cultivar_name': 'Globosum'})
#     assert 'Globosum' == response.session.get('cultivar_name')
#
#
# @pytest.mark.django_db
# def test_authorized_plant_edit_descriptions_view(client):
#     """
#     Test PlantEditDescriptions
#
#     - sprawdzenie poprawności edytowania opisów rośliny
#     """
#     user = User.objects.create_user(username='test', password='TestPass')
#     permission = Permission.objects.get(codename='add_botsystgenus')
#     user.user_permissions.add(permission)
#     user.save()
#
#     genus = BotSystGenus.objects.create(lac_name='Acer', pl_name='klon', hybrid=False)
#     species = BotSystSpecies.objects.create(genus=genus, lac_name='platanoides', pl_name='zwyczajny', hybrid=False)
#     body_type = PlantBodyType.objects.create(body_type='Drzewa', lp=1)
#
#     plant = PlntLibraries.objects.create(genus=genus, species=species, body_type=body_type, edible=False)
#
#     client.login(username='test', password='TestPass')
#
#     response = client.post(f'/botanical/edit-descriptions/{plant.id}/', {'botanical': 'Opis botaniczny',
#                                                                          'agree': 'agree1'})
#     plant2 = PlntLibraries.objects.get(id=plant.id)
#     descr = PlantDescriptions.objects.get(id=plant2.description.id)
#     assert 'Opis botaniczny' == descr.botanical
