from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from botanical.models import BotSystGenus, BotSystSpecies


class BotanicalView(View):
    def get(self, request):
        return render(request, 'botanical_base.html')


class BotanicalAddView(View):
    def get(self, request):
        genus_name = request.session.get('genus_name')
        species_name = request.session.get('species_name')

        if genus_name:
            try:
                gen = BotSystGenus.objects.get(lac_name=genus_name)
            except BotSystGenus.DoesNotExist:
                del request.session['genus_name']
                del request.session['species_name']
                species_name = None

        if species_name:
            try:
                spec = BotSystSpecies.objects.get(genus=gen, lac_name=species_name)
            except BotSystSpecies.DoesNotExist:
                del request.session['species_name']
                species = BotSystSpecies.obiecjs.filter(genus=gen)
                return render(request, 'botanical_sel_species.html', {'genus': gen,
                                                                      'species': species})
            # return render(request, 'botanical_sel_cultivar.html', {'genus': gen,
            #                                                        'spec': spec})

        genus = BotSystGenus.objects.all()
        return render(request, 'botanical_sel_genus.html', {'genus': genus, })

    def post(self, request):
        error = []
        if not request.session.get('genus_name'):
            genus_name = request.POST.get('genus_name')
            if genus_name and genus_name != 'Wybierz':
                request.session['genus_name'] = genus_name
            else:
                error.append('Nie wybrano nazwy Rodzaju')
                genus = BotSystGenus.objects.all()
                return render(request, 'botanical_sel_genus.html', {'genus': genus,
                                                                    'step': 'genus',
                                                                    'error': error})




class BotanicalAddGenusView(View):
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
            error.append('Obie nazwy są wymagane, jeśli polska nazwa nie istnieje to wpisz łacińską z małej litery.')

        return render(request, 'botanical_add_genus.html', {'error': error,
                                                            'genus_lac': genus_lac,
                                                            'genus_pl': genus_pl})
