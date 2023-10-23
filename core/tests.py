import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

from django.http.request import HttpRequest
from django.http.response import HttpResponse

from typing import Dict, Optional
change_form_template = "admin/import_file.html"

    def cria_df(self, pk):
        pd.options.mode.chained_assignment = None
        # Passo 1: Escolher um ativo
        ativo = 'PETR4.SA'
        # Passo 2: Puxar os dados do Yahoo Finance
        dados_ativo = yf.download(ativo)
        
        #tome cuidado com ações muito antigas! As vezes vão ter os dados mas com volume zero. 
        #Pegue um período que tenha volume 
        dados_ativo['Adj Close'].plot()
        
        # Passo 3: Calcular os retornos
        dados_ativo['retornos'] = dados_ativo['Adj Close'].pct_change().dropna() 
        
        # Passo 4: Separar os retornos positivos dos negativos
        retorno = 2
        filtrando_retorno = lambda x: x if x > 0 else 0
        filtrando_retorno(retorno)

        dados_ativo['retornos_postivos'] = dados_ativo['retornos'].apply(lambda x: x if x > 0 else 0)
        dados_ativo['retornos_negativos'] = dados_ativo['retornos'].apply(lambda x: abs(x) if x < 0 else 0)

        # Passo 5: Calcular a média de retornos positivos e negativos dos últimos 22 dias 

        dados_ativo['media_retornos_positivos'] = dados_ativo['retornos_postivos'].rolling(window = 22).mean()
        dados_ativo['media_retornos_negativos'] = dados_ativo['retornos_negativos'].rolling(window = 22).mean()

        dados_ativo = dados_ativo.dropna()

        # Passo 6: Calcular o RSI 

        ### Fórmula RSI:

        # $100 - 100/(1 + mediaRetornosPositivos / mediaRetornosNegativos)$

        dados_ativo['RSI'] = (100 - 100/
                                (1 + dados_ativo['media_retornos_positivos']/dados_ativo['media_retornos_negativos']))

        dados_ativo.head(50)

        # Passo 7: Sinais de compra ou venda

        dados_ativo.loc[dados_ativo['RSI'] < 30, 'compra'] = 'sim'
        dados_ativo.loc[dados_ativo['RSI'] > 30, 'compra'] = 'nao'

        datas_compra = []
        datas_venda = []

        for i in range(len(dados_ativo)):
            if "sim" in dados_ativo['compra'].iloc[i]:
                datas_compra.append(dados_ativo.iloc[i+1].name)
                
        # A gente vai ter 2 stops de venda:

        # * RSI acima de 40
        # * 10 dias de operação

        data_compra = []
        data_venda = []

        for i in range(len(dados_ativo)):
            if "sim" in dados_ativo['compra'].iloc[i]:
                data_compra.append(dados_ativo.iloc[i+1].name) # +1 porque a gente compra no preço de abertura do dia seguinte.
                for j in range(1, 11):
                    if dados_ativo['RSI'].iloc[i + j] > 40: #vendo se nos proximos 10 dias o RSI passa de 40
                        data_venda.append(dados_ativo.iloc[i + j + 1].name) #vende no dia seguinte q bater 40
                        break
                    elif j == 10:
                        data_venda.append(dados_ativo.iloc[i + j + 1].name)

        # Passo 8: Observando pontos de compra ao longo do tempo

        # plt.figure(figsize = (12, 5))
        # plt.scatter(dados_ativo.loc[data_compra].index, dados_ativo.loc[data_compra]['Adj Close'], marker = '^',
        #             c = 'g')
        # plt.plot(dados_ativo['Adj Close'], alpha = 0.7)

        # Passo 9: Calculando lucros

        lucros = dados_ativo.loc[data_venda]['Open'].values/dados_ativo.loc[data_compra]['Open'].values - 1

        # Passo 10: Analisando lucros

        # * Qual a média de lucros?
        # * Qual a média de perdas?
        # * Qual a % de operações vencedoras?
        # * Qual expectativa matemática do modelo?
        # * Qual retorno acumulado?
        # * O retorno acumulado venceu o Buy and Hold na ação?

        operacoes_vencedoras = len(lucros[lucros > 0])/len(lucros)

        operacoes_vencedoras

        media_ganhos = np.mean(lucros[lucros > 0])

        media_ganhos * 100

        media_perdas = abs(np.mean(lucros[lucros < 0]))

        media_perdas

        expectativa_matematica_modelo = (operacoes_vencedoras * media_ganhos) - ((1 - operacoes_vencedoras) * media_perdas)

        expectativa_matematica_modelo * 100

        performance_acumulada = (np.cumprod((1 + lucros)) - 1) 

        performance_acumulada * 100

        # plt.figure(figsize = (12, 5))
        # plt.plot(data_compra, performance_acumulada)

        retorno_buy_and_hold = dados_ativo['Adj Close'].iloc[-1]/dados_ativo['Adj Close'].iloc[0] - 1

        retorno_buy_and_hold * 100
        
        """ abrir um arquivo csv"""
        # file_object = ImportFile.objects.get(pk=pk)
        # df = pd.read_excel(file_object.file.path)
        # var = True

        """ abrir imagem na web"""
        # import webbrowser
        # caminho_imagem = 'caminho/para/meu_grafico.png'
        # webbrowser.open('file://' + caminho_imagem, new=2)

    def change_view(self, request, object_id, extra_context = None):
        extra_context = self.cria_df(pk=object_id)
        return super().change_view(request, object_id, extra_context)