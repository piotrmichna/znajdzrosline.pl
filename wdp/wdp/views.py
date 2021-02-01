from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class Main(View):
    def get(self, request):
        return render(request, 'main_main.html')


class Przeznaczenia(View):
    def get(self, request):
        return render(request, 'main_przeznaczenia.html')
