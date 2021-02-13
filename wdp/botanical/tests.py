import pytest
from django.test import Client
from botanical.models import BotSystGenus, BotSystSpecies, PlantBodyType, PlntLibraries


@pytest.mark.django_db
def test_klient_user_login(klient):
    klient
    c = Client()
    response = c.post('/accounts/login/', {'username': 'Klient', })
    assert response.status_code == 200


@pytest.mark.django_db
def test_klient_user_add_genus(klient):
    c = Client()
    c.force_login(klient)
    response = c.post('/botanical/add/genus/', {'lac_name': 'Acer', 'pl_name': 'klon'})
    assert response.status_code == 403


@pytest.mark.django_db
def test_projektant_user_add_genus(projektant):
    c = Client()
    c.force_login(projektant)
    response = c.post('/botanical/add/genus/', {'genus_lac': 'Acer', 'genus_pl': 'klon'})
    assert response.status_code == 302
    genus = BotSystGenus.objects.get(lac_name='Acer')
    assert genus.lac_name == 'Acer'


@pytest.mark.django_db
def test_klient_user_add_species(klient):
    c = Client()
    c.force_login(klient)
    response = c.post('/botanical/add/species/', {'lac_name': 'platanoides', 'pl_name': 'zwyczajny'})
    assert response.status_code == 403


@pytest.mark.django_db
def test_projektant_user_add_species(projektant):
    c = Client()
    c.force_login(projektant)
    genus = BotSystGenus.objects.create(lac_name='Acer', pl_name='klon')
    session = c.session
    session['genus_name'] = genus.lac_name
    session.save()
    assert c.session.get('genus_name')
    response = c.post('/botanical/add/species/', {'species_lac': 'platanoides', 'species_pl': 'zwyczajny'})
    assert BotSystSpecies.objects.get(lac_name='platanoides')
    assert response.status_code == 302


@pytest.mark.django_db
def test_klient_user_add_body_type(klient):
    c = Client()
    c.force_login(klient)
    response = c.post('/botanical/add/type/', {'body_type': 'Drzewa liściaste', 'lp': 1})
    assert response.status_code == 403


@pytest.mark.django_db
def test_projektant_user_add_body_type(projektant):
    c = Client()
    c.force_login(projektant)
    response = c.post('/botanical/add/type/', {'body_type': 'Drzewa liściaste', 'lp': 1})
    body = PlantBodyType.objects.get(body_type='Drzewa liściaste')
    assert body.body_type == 'Drzewa liściaste'
    assert response.status_code == 302


@pytest.mark.django_db
def test_klient_user_add_plant(klient):
    c = Client()
    c.force_login(klient)
    response = c.post('/botanical/addtype/')
    assert response.status_code == 403


@pytest.mark.django_db
def test_projektant_user_add_plant(projektant):
    c = Client()
    c.force_login(projektant)
    genus = BotSystGenus.objects.create(lac_name='Acerx', pl_name='klon')
    species = BotSystSpecies.objects.create(genus=genus, lac_name='platanoides', pl_name='zwyczajny')
    body_type = PlantBodyType.objects.create(body_type='Drzewa liściaste', lp=1)

    session = c.session
    session['genus_name'] = genus.lac_name
    session['species_name'] = species.lac_name
    session.save()
    plant = PlntLibraries.objects.create(genus=genus,
                                         species=species,
                                         cultivar=None,
                                         body_type=body_type,
                                         edible=False)
    response = c.post('/botanical/addtype/', {'body_type': 'Drzewa liściaste', 'edible': 'Nie'})
    assert PlntLibraries.objects.get(id=plant.id)
    assert response.status_code == 302
