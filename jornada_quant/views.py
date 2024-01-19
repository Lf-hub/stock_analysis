import fundamentus
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

from django.shortcuts import render
from django.views.generic import View

from datetime import datetime, timedelta

# Create your views here.

class IndexView(View):
    template_name = "quant_index.html"

    def get(self, request, *args, **kwargs):
        df = fundamentus.get_resultado()
        df['papel'] = df.index.str[:4]
        df_agrupado = df.drop_duplicates(subset=["papel"]).round(2)
        
        # TODO Criar tabela para armazenar nome ticker se esta ativa ou nao das empresas Filtrar a tabelas pelas astivas

        # df_agrupado['traded_recently'] = df.index.map(lambda papel: self.get_traded_recently(papel))
        # df_filter = df_agrupado[df_agrupado['traded_recently']].round(2)
        data = df_agrupado.to_dict(orient='index')
        return render(request, self.template_name, {'content':data})

    def get_traded_recently(self, papel):
        try:
            ticker = papel+'.SA'
            stock = yf.Ticker(ticker)
            historical_data = stock.history(period='1mo')
            last_day = historical_data.index[-1].date()
            today = datetime.now().date()
            start = today - timedelta(days=5)
            return start <= last_day <= today
        except Exception:
            return False