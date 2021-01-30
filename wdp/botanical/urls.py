from django.urls import path

from botanical.views import BotanicalView, BotanicalAddView

urlpatterns = [
    path('', BotanicalView.as_view(), name='botanical'),
    path('add/', BotanicalAddView.as_view(), name='botanical-add'),
]
