from django.http import HttpResponse
from django.views import View


class Main(View):
    def get(self, request):
        return HttpResponse(f'''
        <h1>Znajdź roślinę</h1>
        <h3><a href="#"></a> Katalog roślin</h3>
        <p>Aplikacja projekt końcowy Django... w CodersLab</p>''')
