from django.urls import path
from core.views import IndexView, APIProcessView, CryptoCurrency

app_name = 'core'


urlpatterns = [
    path('core/',IndexView.as_view(), name='index'),
    path('api_process/<str:param>',APIProcessView.as_view(), name='api_process'),
    path('cripto_moedas/',CryptoCurrency.as_view(), name='cripto_process')
]