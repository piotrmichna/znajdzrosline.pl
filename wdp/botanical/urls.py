from django.urls import path

from botanical.views import (BotanicalView, BotanicalAddView, BotanicalAddGenusView, BotanicalAddSpeciesView,
                             BotanicalAddClear, BotanicalTypeAddView, BotanicalAddTypeView, BotanicalPlantShowView,
                             BotanicalPlantEditView)

urlpatterns = [
    path('', BotanicalView.as_view(), name='botanical'),
    path('show/<int:plant_id>/', BotanicalPlantShowView.as_view(), name='botanical-show'),
    path('edit/<int:plant_id>/', BotanicalPlantEditView.as_view(), name='botanical-edit'),
    path('add/', BotanicalAddView.as_view(), name='botanical-add'),
    path('addtype/', BotanicalTypeAddView.as_view(), name='botanical-type-add'),
    path('add/clear/', BotanicalAddClear.as_view(), name='botanical-add-clear'),
    path('add/genus/', BotanicalAddGenusView.as_view(), name='botanical-add-genus'),
    path('add/species/', BotanicalAddSpeciesView.as_view(), name='botanical-add-species'),
    path('add/type/', BotanicalAddTypeView.as_view(), name='botanical-add-type'),
]
