from django.urls import path
from jornada_quant.views import IndexView

app_name = 'jornada_quant'


urlpatterns = [
    path('',IndexView.as_view(), name='index'),
]