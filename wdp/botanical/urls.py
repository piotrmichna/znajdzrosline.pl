from django.urls import path

from botanical.views import (BotanicalView, BotanicalAddView, BotanicalAddGenusView, BotanicalAddSpeciesView)

urlpatterns = [
    path('', BotanicalView.as_view(), name='botanical'),
    path('add/', BotanicalAddView.as_view(), name='botanical-add'),
    path('add/genus/', BotanicalAddGenusView.as_view(), name='botanical-add-genus'),
    path('add/species/', BotanicalAddSpeciesView.as_view(), name='botanical-add-species'),
]
