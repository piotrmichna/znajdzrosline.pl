from django.urls import path

from botanical.views import (BotanicalView, BotanicalAddView, BotanicalAddGenusView, BotanicalAddSpeciesView,
                             BotanicalAddClear, BotanicalTypeAddView, BotanicalAddTypeView)

urlpatterns = [
    path('', BotanicalView.as_view(), name='botanical'),
    path('add/', BotanicalAddView.as_view(), name='botanical-add'),
    path('addtype/', BotanicalTypeAddView.as_view(), name='botanical-type-add'),
    path('add/clear/', BotanicalAddClear.as_view(), name='botanical-add-clear'),
    path('add/genus/', BotanicalAddGenusView.as_view(), name='botanical-add-genus'),
    path('add/species/', BotanicalAddSpeciesView.as_view(), name='botanical-add-species'),
    path('add/type/', BotanicalAddTypeView.as_view(), name='botanical-add-type'),
]
