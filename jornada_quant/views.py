import fundamentus
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta

from django.shortcuts import render
from django.views.generic import View

from core.models import Companies


# Create your views here.

class IndexView(View):
    template_name = "quant_index.html"

    def get(self, request, *args, **kwargs):
        list_companies = Companies.objects.filter(is_active=True).values_list('slug', flat=True)
        df = fundamentus.get_resultado()
        df['papel'] = df.index.str[:4]
        df_filtrado = df[df.index.isin(list_companies)].round(2)
        df_agrupado = df_filtrado.drop_duplicates(subset=["papel"])
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