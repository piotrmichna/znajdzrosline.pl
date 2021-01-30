from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class BotanicalView(View):
    def get(self, request):
        return render(request, 'botanical_base.html')
