from django.shortcuts import render
from django.views import View


class Main(View):
    """STRONA GŁÓWNA PROJEKTU"""

    def get(self, request):
        return render(request, 'main_main.html')


class Przeznaczenia(View):
    """STRONA PRZEZNACZENIA - KRÓTKI OPIS PRZEZNACZENIA"""

    def get(self, request):
        return render(request, 'main_przeznaczenia.html')


class Kontakt(View):
    """STRONA PRZEZNACZENIA - KRÓTKI OPIS PRZEZNACZENIA"""

    def get(self, request):
        return render(request, 'main_kontakt.html')
