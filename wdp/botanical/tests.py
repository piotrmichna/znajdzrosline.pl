import pytest
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from botanical.models import BotSystGenus, BotSystSpecies, BotSystCultivar, PlantBodyType, PlantDescriptions, \
    PlntLibraries


class ModelBotSystGenusTest(TestCase):
    """ TEST MODELU BotSystGenus """

    def test_genus_create(self):
        genus = BotSystGenus.objects.create(lac_name='Acer', pl_name='klon', hybrid=False)
        genus_check = BotSystGenus.objects.get(lac_name='Acer')

        self.assertEqual(genus.lac_name, genus_check.lac_name)


class ModelBotSystSepciesTest(TestCase):
    """ TEST MODELU BotSystSpecies """

    def test_species_create(self):
        genus = BotSystGenus.objects.create(lac_name='Acer', pl_name='klon', hybrid=False)
        species = BotSystSpecies.objects.create(genus=genus, lac_name='platanoides', pl_name='zwyczajny', hybrid=False)
        species_check = BotSystSpecies.objects.get(lac_name='platanoides')

        self.assertEqual(species.lac_name, species_check.lac_name)


class ModelBotSystCultivarTest(TestCase):
    """ TEST MODELU BotSystCultivar """

    def test_cultivar_create(self):
        genus = BotSystGenus.objects.create(lac_name='Acer', pl_name='klon', hybrid=False)
        species = BotSystSpecies.objects.create(genus=genus, lac_name='platanoides', pl_name='zwyczajny', hybrid=False)
        cultivar = BotSystCultivar.objects.create(species=species, cultivar='Globosum')
        cultivar_check = BotSystCultivar.objects.get(cultivar='Globosum')

        self.assertEqual(cultivar.cultivar, cultivar_check.cultivar)


class ModelPlantBodyTypeTest(TestCase):
    """ TEST MODELU PlantBodyType """

    def test_plant_body_create(self):
        body = PlantBodyType.objects.create(body_type='Drzewa liściaste', lp=1)
        body_check = PlantBodyType.objects.get(body_type='Drzewa liściaste')

        self.assertEqual(body.body_type, body_check.body_type)


class ModelPlantDescriptionsTest(TestCase):
    """ TEST MODELU PlantDescriptions """

    def test_plant_descriptions_create(self):
        descriptions = PlantDescriptions.objects.create(botanical='Opis...')
        description_check = PlantDescriptions.objects.get(botanical='Opis...')

        self.assertEqual(descriptions.botanical, description_check.botanical)


class ModelPlntLibrariesTest(TestCase):
    """ TEST MODELU PlntLibraries """

    def test_plant_create(self):
        genus = BotSystGenus.objects.create(lac_name='Acer', pl_name='klon', hybrid=False)
        species = BotSystSpecies.objects.create(genus=genus, lac_name='platanoides', pl_name='zwyczajny', hybrid=False)
        body_type = PlantBodyType.objects.create(body_type='Drzewa', lp=1)

        plant = PlntLibraries.objects.create(genus=genus, species=species, body_type=body_type, edible=False)
        plant_check = PlntLibraries.objects.get(genus=genus)

        self.assertEqual(plant.genus, plant_check.genus)


class GetBotanicalViewTest(TestCase):
    """
    TEST WIDOKU BotanicalView

    test dostępności głównego widoku katalogu roślin dla użytkowników nie zalogowanych
    """

    def test_get_botanical_view(self):
        response = self.client.get(reverse('botanical'))
        self.assertEqual(response.status_code, 200)


class GetBotanicalSystAddViewTest(TestCase):
    """
    TEST WIDOKU BotanicalSystAdd

    test dostępności widoku katalogu dodawania roślin dla użytkowników nie zalogowanych
    """

    def test_get_botanical_add_no_login_user(self):
        response = self.client.get(reverse('botanical-add'))
        self.assertEqual(response.status_code, 302)


class LoginViewTest(TestCase):
    """TEST LOGOWANIA"""

    def test_post_login_view(self):
        user = User.objects.create_user('test', 'test@test.com', 'Testpass')

        response = self.client.post(reverse('login'), {'username': 'test', 'password': 'Testpass'})
        self.assertEqual(response.status_code, 302)  # użytkownik zalogowany bez uprawnień


@pytest.mark.django_db
def test_post_no_authorized_genus_view(client):
    user = User.objects.create_user('test')

    client.force_login('test')
    response = client.post('/botanical/add/genus/', {'lac_name': 'Fraxinus', 'pl_name': 'jesion'})
    assert response.status_code == 403


@pytest.mark.django_db
def test_post_authorized_genus_view(client):
    user = User.objects.create_user(username='test', password='TestPass')
    permission = Permission.objects.get(codename='add_botsystgenus')
    user.user_permissions.add(permission)
    user.save()

    client.login(username='test', password='TestPass')
    response = client.post('/botanical/add/genus/', {'lac_name': 'Fraxinus', 'pl_name': 'jesion'})

    assert BotSystGenus.objects.get(lac_name='Fraxinus')


@pytest.mark.django_db
def test_post_authorized_species_view(client):
    """TEST DODAWANIA NAZW GATUNKÓW"""
    user = User.objects.create_user(username='test', password='TestPass')
    permission = Permission.objects.get(codename='add_botsystgenus')
    user.user_permissions.add(permission)
    user.save()

    client.login(username='test', password='TestPass')
    response = client.post('/botanical/add/species/', {'lac_name': 'excelsrior', 'pl_name': 'wyniosły'})

    assert BotSystGenus.objects.get(lac_name='excelsrior')



@pytest.mark.django_db
def test_authorized_botanical_add_type_view(client):
    """
    Test BotanicalAddTypeView

    - sprawdzenie poprawności dodawania unikalnych nazw typów rośliny
    _ sprawdzenie zwracania komunikatu error po ponownym dodaniu tej samej rośliny
    """
    user = User.objects.create_user(username='test', password='TestPass')
    permission = Permission.objects.get(codename='add_botsystgenus')
    user.user_permissions.add(permission)
    user.save()
    client.login(username='test', password='TestPass')

    response = client.post('/botanical/add/type/', {'body_type': 'Rośliny zielne'})
    assert PlantBodyType.objects.get(body_type='Rośliny zielne')

    response = client.post('/botanical/add/type/', {'body_type': 'Rośliny zielne'})
    assert len(response.error) > 0


def test_authorized_botanical_syst_add_view(client):
    """
    Test BotanicalSystAddView

    sprawdzenie zmiennej sesyjnej ustawianej po wyborze gatunku
    """
    user = User.objects.create_user(username='test', password='TestPass')
    permission = Permission.objects.get(codename='add_botsystgenus')
    user.user_permissions.add(permission)
    user.save()

    client.login(username='test', password='TestPass')
    response = client.post('/botanical/add/', {'genus_name': 'Acer'})
    assert 'Acer' == response.session.get('genus_name')

    response = client.post('/botanical/add/', {'species_name': 'platanus'})
    assert 'platanus' == response.session.get('species_name')

    response = client.post('/botanical/add/', {'cultivar_name': 'Globosum'})
    assert 'Globosum' == response.session.get('cultivar_name')


@pytest.mark.django_db
def test_authorized_plant_edit_descriptions_view(client):
    """
    Test PlantEditDescriptions

    - sprawdzenie poprawności edytowania opisów rośliny
    """
    user = User.objects.create_user(username='test', password='TestPass')
    permission = Permission.objects.get(codename='add_botsystgenus')
    user.user_permissions.add(permission)
    user.save()

    genus = BotSystGenus.objects.create(lac_name='Acer', pl_name='klon', hybrid=False)
    species = BotSystSpecies.objects.create(genus=genus, lac_name='platanoides', pl_name='zwyczajny', hybrid=False)
    body_type = PlantBodyType.objects.create(body_type='Drzewa', lp=1)

    plant = PlntLibraries.objects.create(genus=genus, species=species, body_type=body_type, edible=False)

    client.login(username='test', password='TestPass')

    response = client.post(f'/botanical/edit-descriptions/{plant.id}/', {'botanical': 'Opis botaniczny',
                                                                         'agree': 'agree1'})
    plant2 = PlntLibraries.objects.get(id=plant.id)
    descr = PlantDescriptions.objects.get(id=plant2.description.id)
    assert 'Opis botaniczny' == descr.botanical
