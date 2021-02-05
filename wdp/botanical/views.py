from math import ceil
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import F
from django.shortcuts import render, redirect
from django.views import View

from botanical.models import (BotSystGenus, BotSystSpecies, BotSystCultivar, PlantBodyType, PlntLibraries,
                              PlantDescriptions)


class BotanicalView(View):
    """WIDOK GŁÓWNY KATALOGU ROŚLIN"""

    def get(self, request):
        plant_num = PlntLibraries.objects.count()
        return render(request, 'botanical_main.html', {'plant_num': plant_num})


class BotanicalPlantShowView(View):
    """WIDOK WYŚWIETLA SZCZEGÓŁOWE INFORMACJE O ROŚLINIE"""

    def get(self, request, plant_id):
        try:
            plant = PlntLibraries.objects.get(id=plant_id)
        except PlntLibraries.DoesNotExist:
            plant = None

        return render(request, 'botanical_show.html', {'plant': plant})


class BotanicalSystAddView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    WIDOK DODAWANIA NAZW ROŚLIN

    klasa udostępnia kolejne szablony wyboru członów nazwy i zapisuje wybrane w
    zmiennych sesyjnych (genus, species, cultivar)

    Nazwa rośliny = genus (wymagany)
                        `- species
                                `- cultivar
    Metody
    ------
    get - Wyświetla odpowiedni szablon adekwatny dla nie wybranego poziomu nazwy,
        na podstawie zmiennych sesyjnych przechowujących wybranych już nazw.
        - Szablony dla poziomów nazw (genus i species) zawierają posiadają pole
        typu <select> wyboru nazwy oraz odnośnik do odrębnego szablonu dodawania nowych.
        - Nazwa cultivar jest nazwą indywidualną rośliny więc szablo dla tego poziomu
        zawiera pole typu <input>

    post - Obsługuje formularze szablonów kolejno dla poziomów nazw, przy pozytywnej
        walidacji ustawia zmienną sesyjną dla danego poziomu i wyświetla szablon
        kolejnego poziomu.
        - szablony species i cultivar zawierają dwa formularze ( wybór nazwy dla poziomu,
        zapis pełnej nazwy), wysłanie formularza pełnej nazwy kończy działanie widoku i
        przekierowuje na adres widoku definiowania cech rośliny.
    """
    permission_required = ('botanical.add_botsystgenus', 'botanical.add_botsystspecies')

    def get(self, request):
        genus_name = request.session.get('genus_name')
        species_name = request.session.get('species_name')

        if genus_name:  # ETAP WYBORU RODZAJU
            try:
                gen = BotSystGenus.objects.get(lac_name=genus_name)
            except BotSystGenus.DoesNotExist:
                del request.session['genus_name']
                del request.session['species_name']
                genus = BotSystGenus.objects.all()
                return render(request, 'botanical_sel_genus.html', {'genus': genus})

            if species_name:  # ETAP WYBORU ODMIANY
                try:
                    species = BotSystSpecies.objects.get(genus=gen, lac_name=species_name)
                except BotSystSpecies.DoesNotExist:
                    del request.session['species_name']
                    species = BotSystSpecies.objects.filter(genus=gen)
                    return render(request, 'botanical_sel_species.html', {'genus': gen,
                                                                          'species': species})

                return render(request, 'botanical_sel_cultivar.html', {'genus': gen,
                                                                       'spec': species})
            else:  # ETAP WYBORU GATUNKU
                species = BotSystSpecies.objects.filter(genus=gen)
                return render(request, 'botanical_sel_species.html', {'genus': gen,
                                                                      'species': species})

        genus = BotSystGenus.objects.all()
        return render(request, 'botanical_sel_genus.html', {'genus': genus, })

    def post(self, request):
        error = []
        plant_name = request.POST.get('plant_name')
        if plant_name and request.session.get('genus_name'):  # KONIEC DEFINIOWANIA PEŁNEJ NAZWY
            return redirect('botanical-type-add')

        if not request.session.get('genus_name'):  # WYBÓR NAZWY RODZAJU
            genus_name = request.POST.get('genus_name')
            if genus_name and genus_name != 'Wybierz':
                try:
                    genus = BotSystGenus.objects.get(lac_name=genus_name)
                except BotSystGenus.DoesNotExist:
                    error.append("Nie istnieje rodzaj z taką nazwą łacińską.")
                    genus = BotSystGenus.objects.all()
                    return render(request, 'botanical_sel_genus.html', {'genus': genus,
                                                                        'genus_name': genus_name,
                                                                        'error': error})

                request.session['genus_name'] = genus_name  # KONIEC WYBÓR NAZWY RODZAJU
                species = BotSystSpecies.objects.filter(genus=genus)
                return render(request, 'botanical_sel_species.html', {'genus': genus,
                                                                      'species': species})
            else:
                error.append('Nie wybrano nazwy Rodzaju')
                genus = BotSystGenus.objects.all()
                return render(request, 'botanical_sel_genus.html', {'genus': genus,
                                                                    'error': error})
        elif not request.session.get('species_name'):  # WYBÓR NAZWY GATUNKU

            genus_name = request.session.get('genus_name')
            try:
                genus = BotSystGenus.objects.get(lac_name=genus_name)
            except BotSystGenus.DoesNotExist:
                error.append("Nie istnieje rodzaj z taką nazwą łacińską.")
                del request.session['genus_name']
                genus = BotSystGenus.objects.all()
                return render(request, 'botanical_sel_genus.html', {'genus': genus,
                                                                    'error': error})
            species_name = request.POST.get('species_name')
            if species_name and species_name != 'Wybierz':
                try:
                    species = BotSystSpecies.objects.get(genus=genus, lac_name=species_name)
                except BotSystSpecies.DoesNotExist:
                    error.append(f"Nie istnieje gatunek z taką nazwą łacińską dla rodzaju: {genus.lac_name}.")
                    species = BotSystSpecies.objects.filter(genus=genus).all()
                    return render(request, 'botanical_sel_species.html', {'genus': genus,
                                                                          'species': species,
                                                                          'error': error})
                request.session['species_name'] = species_name  # KONIEC WYBÓR NAZWY GATUNKU
                cultivar = BotSystCultivar.objects.filter(species=species)
                return render(request, 'botanical_sel_cultivar.html', {'genus': genus,
                                                                       'species': species,
                                                                       'cultivar': cultivar})
            else:
                species = BotSystSpecies.objects.filter(genus=genus).all()
                return render(request, 'botanical_sel_species.html', {'genus': genus,
                                                                      'species': species})
        else:  # WYBÓR NAZWY ODMIANY
            genus = BotSystGenus.objects.get(lac_name=request.session.get('genus_name'))
            species = BotSystSpecies.objects.get(genus=genus, lac_name=request.session.get('species_name'))
            cultivar_name = request.POST.get('cultivar_name')
            if cultivar_name:
                if not BotSystCultivar.objects.filter(species=species, cultivar=cultivar_name).count():
                    request.session['cultivar_name'] = cultivar_name  # KONIEC WYBÓR NAZWY GATUNKU
                else:
                    error.append('Roślina o tej odmianie już istnieje!')
            return render(request, 'botanical_sel_cultivar.html', {'genus': genus,
                                                                   'species': species,
                                                                   'cultivar': cultivar_name,
                                                                   'error': error})


class BotanicalAddGenusView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
        WIDOK DODAWANIA NAZW RODZAJU

        Definiowanie nowych nazw rodzaju, zapewnienie unikalności nazw.
        """
    permission_required = ('botanical.add_botsystgenus')

    def get(self, request):
        return render(request, 'botanical_add_genus.html')

    def post(self, request):
        genus_lac = request.POST.get('genus_lac')
        genus_pl = request.POST.get('genus_pl')
        error = []
        if len(genus_lac) and len(genus_pl):
            if genus_lac[0] == 'x' or genus_pl[0] == 'x':
                if genus_lac[0] != 'x' or genus_pl[0] != 'x':
                    error.append("Dla mieszańca obie nazwy powinna poprzedzać litera x.")
                else:
                    lac = genus_lac.split(' ')
                    pl = genus_pl.split(' ')
                    if not BotSystGenus.objects.filter(lac_name=lac[1], pl_name=pl[1], hybrid=True).count():
                        BotSystGenus.objects.create(lac_name=lac[1], pl_name=pl[1], hybrid=True)
                        return redirect('/botanical/add/')
                    else:
                        error.append('W katalogu już istniej Rodzaj o takich nazwach.')
            else:
                if not BotSystGenus.objects.filter(lac_name=genus_lac, pl_name=genus_pl).count():
                    BotSystGenus.objects.create(lac_name=genus_lac, pl_name=genus_pl, hybrid=False)
                    return redirect('/botanical/add/')
                else:
                    error.append('W katalogu już istniej Rodzaj o takich nazwach.')
        else:
            error.append(
                'Obie nazwy są wymagane, jeśli polska nazwa nie istnieje to wpisz łacińską z małej litery.')

        return render(request, 'botanical_add_genus.html', {'error': error,
                                                            'genus_lac': genus_lac,
                                                            'genus_pl': genus_pl})


class BotanicalAddSpeciesView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    DODAWANIE NAZW GATUNKU

    Dodawanie nowych unikalnych nazw gatunku należących do zbioru danego rodzaju.
    """
    permission_required = ('botanical.add_botsystgenus')

    def get(self, request):
        genus_name = request.session.get('genus_name')

        if genus_name:
            return render(request, 'botanical_add_species.html', {'genus_name': genus_name})
        else:
            return redirect('/botanical/add/')

    def post(self, request):
        error = []
        try:
            genus = BotSystGenus.objects.get(lac_name=request.session.get('genus_name'))
        except BotSystGenus.DoesNotExist:
            return redirect('/botanical/add/')
        species_lac = request.POST.get('species_lac')
        species_pl = request.POST.get('species_pl')

        if not species_lac or not species_pl:
            error.append('Obnie nazwy są wymagane.')
        else:
            if BotSystSpecies.objects.filter(genus=genus, lac_name=species_lac, pl_name=species_pl).count():
                error.append('Gatunek o takich nazwach już istnieje!')
            else:
                BotSystSpecies.objects.create(genus=genus, lac_name=species_lac, pl_name=species_pl)
                return redirect('/botanical/add/')

        return render(request, 'botanical_add_species.html', {'genus_name': request.session.get('genus_name'),
                                                              'species_lac': species_lac,
                                                              'species_pl': species_pl,
                                                              'error': error})


class BotanicalTypeAddView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    WIDOK DODAWANIA CECH ROŚLINY

    Widok udostępnia szablon wyboru typu pokroju oraz przydatności do spożycia rośliny.
    Po poprawnej walidacji wartości formularza łącznie z nazwą rośliny zapisaną w sesji
    następuje stworzenie obiektu PlntLibraries oraz usunięcie zmiennych sesyjnych nazwy.
    """

    permission_required = ('botanical.add_botsystgenus')

    def get(self, request):
        plant_name = request.session.get('genus_name')
        if not plant_name:
            return redirect('botanical')

        body_types = PlantBodyType.objects.all()

        plant_name += f" {request.session.get('species_name')}"
        if request.session.get('cultivar_name'):
            plant_name += f" {request.session.get('cultivar_name')}"
        return render(request, 'botanical_sel_type.html', {'body_types': body_types,
                                                           'plant_name': plant_name})

    def post(self, request):
        body_type = request.POST.get('body_type')
        edible = request.POST.get('edible')

        error = []
        if body_type:
            try:
                body = PlantBodyType.objects.get(body_type=body_type)
            except PlantBodyType.DoesNotExist:
                error.append('Wybierz nazwę typu.')
                body = None

        if edible:
            if edible == "Tak":
                edible = True
            else:
                edible = False

            if body:
                valid = False
                if request.session.get('genus_name'):
                    try:
                        genus = BotSystGenus.objects.get(lac_name=request.session['genus_name'])
                        valid = True
                    except BotSystGenus.DoesNotExist:
                        valid = False
                        error.append("Błędna nazwa rodzaju")

                if request.session.get('species_name') and valid:
                    try:
                        species = BotSystSpecies.objects.get(genus=genus, lac_name=request.session['species_name'])
                    except BotSystSpecies.DoesNotExist:
                        valid = False
                        species = None
                        error.append("Błędna nazwa gatunku")
                elif valid:
                    species = None

                if request.session.get('cultivar_name') and species:
                    if BotSystCultivar.objects.filter(species=species,
                                                      cultivar=request.session['cultivar_name']).count():
                        error.append('Roślina o podanej odmianie zoostała już dodana')
                        valid = False
                    else:
                        cultivar = BotSystCultivar.objects.create(species=species,
                                                                  cultivar=request.session['cultivar_name'])
                else:
                    cultivar = None

                if valid:
                    if request.session.get('genus_name'):
                        del request.session['genus_name']
                    if request.session.get('species_name'):
                        del request.session['species_name']
                    if request.session.get('cultivar_name'):
                        del request.session['cultivar_name']
                    plant = PlntLibraries.objects.create(genus=genus,
                                                         species=species,
                                                         cultivar=cultivar,
                                                         body_type=body,
                                                         edible=edible)
                    return redirect(f'/botanical/show/{plant.id}/')

        else:
            edible = None
            error.append('nie wybrano przydatność do jedzenia.')

        body_types = PlantBodyType.objects.all()
        plant_name = request.POST.get('plant_name')
        return render(request, 'botanical_sel_type.html', {'body_type': body_type,
                                                           'body_types': body_types,
                                                           'plant_name': plant_name,
                                                           'edible': edible,
                                                           'error': error})


class BotanicalAddTypeView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    DODAWANIE TYPÓW POKROJU

    Wyświetla formularz dodawania nowych typów rośliny.
    Umiemożliwa wystąpienia powtórzeń nazw.
    """
    permission_required = ('botanical.add_botsystgenus')

    def get(self, request):
        return render(request, 'botanical_add_body_type.html')

    def post(self, request):
        body_type = request.POST.get('body_type')
        error = []
        if len(body_type) > 4:
            if PlantBodyType.objects.filter(body_type=body_type).count():
                error.append('Typ już istnieje')
            else:
                lp = PlantBodyType.objects.all().count()
                lp += 1
                PlantBodyType.objects.create(body_type=body_type, lp=lp)
                return redirect('botanical-type-add')
        else:
            error.append("Nie wypełniono typu lub jest krótszy niż 5 liter.")
            return render(request, 'botanical_add_body_type.html', {'body_type': body_type,
                                                                    'error': error})


class BotanicalAddClear(LoginRequiredMixin, View):
    """WIDOK USUWA NAZWY ROŚLINY Z SESJI W PRZYPADKU REZYGNACJI Z DODAWANIA DANEJ ROŚLINY"""

    def get(self, request):
        if request.session.get('genus_name'):
            del request.session['genus_name']
        if request.session.get('species_name'):
            del request.session['species_name']
        if request.session.get('cultivar_name'):
            del request.session['cultivar_name']
        return redirect('botanical')


class BotanicalPlantEditView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """WIDOK WYŚWIETLA SZCZEGÓŁY ROŚLINY + ZAWIERA ODNOŚNIKI DO EDYCJI OPISÓW I CECH ROŚLINY"""

    permission_required = ('botanical.add_botsystgenus')

    def get(self, request, plant_id):
        try:
            plant = PlntLibraries.objects.get(id=plant_id)
        except PlntLibraries.DoesNotExist:
            plant = None

        return render(request, 'botanical_edit.html', {'plant': plant})


class PlantEditDescriptions(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    WIDOK EDYCJI OPISÓW ROŚLINY

    Klasa umożliwia edycję opisów: botaniczny, uprawa, zastosowanie.
    Opis botaniczny jest wymagany.

    metody
    ------
    get - wyświetla szablon z formularzem dla wszystkich opisów wypełnionych aktualnym stanem.

    post - Sprawdza zawartość odebranych pól z formularza (raz wypełniony opis można modyfikować
            z wyjątkiem pustego)
         - W przypadku braku opisów dla uprawy i zastosowania metoda wymaga dodatkowego potwierdzenia
         - Zapisuje wprowadzone zmiany.
    """
    permission_required = ('botanical.add_botsystgenus')

    def get(self, request, plant_id):
        try:
            plant = PlntLibraries.objects.get(id=plant_id)
        except PlntLibraries.DoesNotExist:
            plant = None
        descriptions = {}
        if plant:
            if plant.description:
                descriptions = {'botanical': plant.description.botanical,
                                'cultivation': plant.description.cultivation,
                                'destiny': plant.description.destiny}

        return render(request, 'botanical_edit_description.html', {'plant': plant,
                                                                   'descriptions': descriptions})

    def post(self, request, plant_id):
        error = []
        descriptions = {}
        try:
            plant = PlntLibraries.objects.get(id=plant_id)
        except PlntLibraries.DoesNotExist:
            plant = None
            error.append('Nie znaleziono rośliny.')

        if plant:
            if plant.description:
                description = PlantDescriptions.objects.get(id=plant.description.id)
            else:
                description = PlantDescriptions()
            if request.POST.get('destiny'):
                descriptions['destiny'] = request.POST.get('destiny')
                description.destiny = request.POST.get('destiny')
            else:
                error.append("Nie wypełniono opisu zastosowania.")

            if request.POST.get('cultivation'):
                descriptions['cultivation'] = request.POST.get('cultivation')
                description.cultivation = request.POST.get('cultivation')
            else:
                error.append("Nie wypełniono opisu uprawy.")

            if request.POST.get('botanical'):
                descriptions['botanical'] = request.POST.get('botanical')
                description.botanical = request.POST.get('botanical')
                descriptions['agree'] = 'agree1'
            else:
                error.append("Nie wypełniono opisu botanicznego. Jest wymagany!")

            if len(error) == 0 or 'agree1' == request.POST.get('agree'):
                description.save()
                if not plant.description:
                    plant.description = description
                    plant.save()
                return redirect('/botanical/list/1/')

        return render(request, 'botanical_edit_description.html', {'plant': plant,
                                                                   'descriptions': descriptions,
                                                                   'error': error})


class PlantEditBody(LoginRequiredMixin, PermissionRequiredMixin, View):
    """EDYCJA CECH ROŚLINY"""

    permission_required = ('botanical.add_botsystgenus')

    def get(self, request, plant_id):
        try:
            plant = PlntLibraries.objects.get(id=plant_id)
        except PlntLibraries.DoesNotExist:
            plant = None

        edible = ''
        if plant:
            body_type = plant.body_type.body_type
            if plant.edible:
                edible = 'checked'

        body_types = PlantBodyType.objects.order_by('lp').all()
        return render(request, 'botanical_edit_body.html', {'plant': plant,
                                                            'body_types': body_types,
                                                            'body_type': body_type,
                                                            'edible': edible})

    def post(self, request, plant_id):
        try:
            plant = PlntLibraries.objects.get(id=plant_id)
        except PlntLibraries.DoesNotExist:
            plant = None

        error = []
        if plant:
            change = 0
            body_type = request.POST.get('body_type')
            if request.POST.get('body_type'):
                if plant.body_type.body_type != request.POST.get('body_type'):
                    try:
                        plant.body_type = PlantBodyType.objects.get(body_type=request.POST.get('body_type'))
                        change += 1
                    except PlantBodyType.DoesNotExist:
                        error.append('Brak typu rośliny.')
            edible = request.POST.get('edible')
            if edible:
                if not plant.edible:
                    plant.edible = True
                    change += 1
            else:
                if plant.edible:
                    plant.edible = False
                    change += 1
            if change:
                plant.save()
                return redirect('/botanical/list/1/')
            else:
                error.append('Nie wprowadzono zmian.')

        body_types = PlantBodyType.objects.order_by('lp').all()
        return render(request, 'botanical_edit_body.html', {'plant': plant,
                                                            'body_types': body_types,
                                                            'body_type': body_type,
                                                            'edible': edible,
                                                            'error': error})


class BotanicalPlantDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    USUWANIE ROŚLINY

    Widok usuwa istniejące rośliny z katalogu

    get -Wyświetla szablon z informacjami o roślinie
    post - Wyświetla szablon z informacjami oraz formularz usunięcia rośliny
    """
    permission_required = ('botanical.add_botsystgenus')

    def get(self, request, plant_id):
        try:
            plant = PlntLibraries.objects.get(id=plant_id)
        except PlntLibraries.DoesNotExist:
            plant = None

        return render(request, 'botanical_delete.html', {'plant': plant})

    def post(self, request, plant_id):
        if request.POST.get('plant_delete'):
            plant = PlntLibraries.objects.get(id=plant_id)
            if plant.cultivar:
                cultivar = BotSystCultivar.objects.get(id=plant.cultivar.id)
                cultivar.delete()

            plant.delete()
            return redirect('botanical')

        try:
            plant = PlntLibraries.objects.get(id=plant_id)
        except PlntLibraries.DoesNotExist:
            plant = None
        return render(request, 'botanical_delete.html', {'plant': plant,
                                                         'plant_delete': 'tak'})


class BotanicalListView(View):
    """
    LISTA ROŚLIN

    Wyświetla listę roślin istniejących w katalogu.
    Wiersze roślin zawierają odnośniki dla osób zalogowanych wyświetlają wszystkie działania a
    dla osób nie zalogowanych widoczne jest tylko wyświetlanie szczegółów rośliny.

    """

    def get(self, request, page):

        # plants1 = PlntLibraries.objects.filter(cultivar__isnull=True).order_by('genus__lac_name',
        #                                                                        'species__lac_name')
        # plants = plants1.union(plants2)
        plants_num = PlntLibraries.objects.order_by('genus__lac_name',
                                                    F('species__lac_name').desc(nulls_last=False),
                                                    F('cultivar__cultivar').desc(nulls_last=False)).count()
        if not page:
            page = 1
        paginator = {}
        plants_on_page = 5
        if plants_num == 0:
            plants_num = 1
        paginator['page_num'] = ceil(plants_num / plants_on_page)
        if (paginator['page_num'] > 0) and (page > paginator['page_num']):
            page = paginator['page_num']
        paginator['page'] = page
        if paginator['page_num'] > 1:
            paginator['page_prev'] = page - 1
            paginator['page_next'] = page + 1
            paginator['page_nav'] = []
            for st in range(1, paginator['page_num'] + 1):
                paginator['page_nav'].append(st)

        plants = PlntLibraries.objects.order_by('genus__lac_name',
                                                F('species__lac_name').desc(nulls_last=False),
                                                F('cultivar__cultivar').desc(nulls_last=False))[
                 (page - 1) * plants_on_page:page * plants_on_page]

        return render(request, 'botanical_list.html', {'plants': plants, 'paginator': paginator})
