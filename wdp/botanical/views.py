from django.http import HttpResponse
from django.views import View


class BotanicalView(View):
    def get(self, request):
        return HttpResponse('<h1>Botanical</h1>')
