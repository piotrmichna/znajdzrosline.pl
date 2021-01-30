from django.urls import path

from botanical.views import BotanicalView

urlpatterns = [
    path('', BotanicalView.as_view(), name='botanical'),
]
