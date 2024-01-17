import fundamentus
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

from django.shortcuts import render
from django.views.generic import View

# Create your views here.

class IndexView(View):
    template_name = "quant_index.html"

    def get(self, request, *args, **kwargs):
        df = fundamentus.get_resultado()
        df['papel'] = df.index.str[:4]
        df_agrupado = df.drop_duplicates(subset=["papel"])
        # TODO criar funcao onde verifica as ações que ainda estao ativas
        df_agrupado = df_agrupado.round(2)
        data = df_agrupado.to_dict(orient='index')
        return render(request, self.template_name, {'content':data})
