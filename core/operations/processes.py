import os
import requests
import datetime
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

from statsmodels.tsa.stattools import coint

from sklearn import linear_model
from sklearn.metrics import r2_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.feature_selection import SelectKBest
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

class ConsultAPI:
    
    @staticmethod
    def get_content_coingecko():
        url = "https://api.coingecko.com/api/v3/coins/bitcoin"
        response = requests.get(url)
        data = response.json()

    def main(self):
        self.get_content_coingecko()


class ConsultYahoo:
    
    @staticmethod
    def get_data(asset_list, start_dt, end_dt):
        data = pd.DataFrame()
        for i in range(len(asset_list)):
            d=yf.download(asset_list[i],start_dt,end_dt)
            d=d['Adj Close']
            n=asset_list[i]
            data[n]=d
        return data
    
    @staticmethod
    def find_coint_pairs(data,pv):
        n = data.shape[1]
        score_matrix = np.zeros((n, n))
        pvalue_matrix = np.ones((n, n))
        keys = data.keys()
        pairs = []
        for i in range(n):
            for j in range(i+1, n):
                S1 = data[keys[i]]
                S2 = data[keys[j]]
                result = coint(S1, S2)
                score = result[0]
                pvalue = result[1]
                score_matrix[i, j] = score
                pvalue_matrix[i, j] = pvalue
                if pvalue < pv:
                    pairs.append((keys[i], keys[j]))
        return score_matrix, pvalue_matrix, pairs
    
    def main(self, asset_list):
        start_dt=datetime.datetime(2016, 1, 1)
        end_dt=datetime.date.today()
        # pega conteudo 
        sdata = self.get_data(asset_list,start_dt,end_dt)
        # ajusta null para 0
        sdata.fillna(0,inplace=True)
        # cria cointegração
        scores, pvalues, pairs=self.find_coint_pairs(sdata,0.05)
        
        p2=pvalues.T
        # Heatmap to show pvalues of cointegration test
        import seaborn
        fig,ax = plt.subplots(figsize=(80,80))
        # seaborn.heatmap(p2,ax=ax, annot=True, fmt='.3g', cbar=False, xticklabels=stocks,yticklabels=stocks,cmap='hot',mask=(p2>=0.95))
        plt.savefig('coint_bovespa50.png')
        plt.show

        print(pairs)

        # Export List of Pairs to Excel
        p=pd.DataFrame(pairs)
        p.to_excel("CointPairs_output.xlsx") 


class ConsultCSV:
    def main():
        pass


class ConsultXLSX:
    def main():
        pass


class PreviewPrice:

    def __init__(self, path):
        self.path = path

    # Função para leitura e pré-processamento dos dados
    def read_and_preprocess_data(self, folder_path):
        dfs = []
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".csv"):
                file_path = os.path.join(folder_path, file_name)
                df = pd.read_csv(file_path, encoding='latin1', sep=';')
                if not df.empty:
                    df = self.preprocess_dataframe(df)
                    dfs.append(df)
        combined_df = pd.concat(dfs)
        return combined_df
    
    def preprocess_dataframe(self, df):
        # Filtra dados relevantes
        df = df[df['Ativo'] != '']

        # Substitui vírgulas por pontos em colunas numéricas
        numeric_cols = ['Abertura', 'Máximo', 'Mínimo', 'Fechamento', 'Volume', 'Quantidade']
        for col in numeric_cols:
            df[col] = df[col].str.replace(',', '.')
            if col in ('Volume', 'Quantidade'):
                df[col] = df[col].str.replace('.', '').str.replace(',', '.')

        # Calcula médias móveis
        df['mm5d'] = df['Fechamento'].rolling(5).mean()
        df['mm21d'] = df['Fechamento'].rolling(21).mean()

        # Remove linhas com valores nulos
        df.dropna(inplace=True)
        
        return df

    # Função para treinamento e previsão de modelos
    @staticmethod
    def train_and_predict_models(df_ativo):
        # #verificando quantidade de linhas
        qtd_linhas = len(df_ativo)

        qtd_linhas_treino= round(.70 * qtd_linhas)
        qtd_linhas_teste= qtd_linhas - qtd_linhas_treino  
        qtd_linhas_validacao = qtd_linhas -20000

        info = (
            f"linhas treino= 0:{qtd_linhas_treino}"
            f" linhas teste= {qtd_linhas_treino}:{qtd_linhas_treino + qtd_linhas_teste -20000}"
            f" linhas validação= {qtd_linhas_validacao}"
        )

        #reindexando o data frame
        df_ativo = df_ativo.reset_index(drop=True)

        # Substituir "," por "." em todas as colunas relevantes
        df_ativo['Abertura'] = df_ativo['Abertura'].str.replace(',', '.')
        df_ativo['Máximo'] = df_ativo['Máximo'].str.replace(',', '.')
        df_ativo['Mínimo'] = df_ativo['Mínimo'].str.replace(',', '.')
        df_ativo['Fechamento'] = df_ativo['Fechamento'].str.replace(',', '.')
        df_ativo['Volume'] = df_ativo['Volume'].str.replace('.', '').str.replace(',', '.')
        df_ativo['Quantidade'] = df_ativo['Quantidade'].str.replace('.', '').str.replace(',', '.')

        #separando as features e labels
        features = df_ativo.drop(['Ativo','Data', 'Fechamento'], axis=1)
        labels = df_ativo['Fechamento']

        #Escolhendo as melhores features com Kbest
        features_list = ('Abertura','Volume','Quantidade','mm5d','mm21d')

        k_best_features = SelectKBest(k='all')
        k_best_features.fit_transform (features, labels)
        k_best_features_scores = k_best_features.scores_
        raw_pairs = zip(features_list[1:], k_best_features_scores)
        ordered_pairs = list(reversed(sorted(raw_pairs, key=lambda x: x[1])))

        k_best_features_final = dict(ordered_pairs[:15])
        best_features = k_best_features_final.keys()

        #separando as features escolhidas
        features = df_ativo.loc[:,['Quantidade','Volume','mm5d']]

        #Separa os dados de treino teste e validação
        X_train = features[:qtd_linhas_treino]
        X_test = features[qtd_linhas_treino:qtd_linhas_treino + qtd_linhas_teste -1]
        y_train = labels[:qtd_linhas_treino]
        y_test = labels[qtd_linhas_treino:qtd_linhas_treino + qtd_linhas_teste -1]

        # Normalizando os dados de entrada(features)
        # Gerando o novo padrão
        scaler = MinMaxScaler()
        X_train_scale = scaler.fit_transform(X_train)  # Normalizando os dados de entrada(treinamento)
        X_test_scale  = scaler.transform(X_test)       

        #treinamento usando regressão linear
        lr = linear_model.LinearRegression()
        lr.fit(X_train_scale, y_train)
        pred= lr.predict(X_test_scale)
        cd =r2_score(y_test, pred)

        #rede neural
        rn = MLPRegressor(max_iter=2000)
        rn.fit(X_train_scale, y_train)
        pred= rn.predict(X_test_scale)
        cd = rn.score(X_test_scale, y_test)
        
        #rede neural com ajuste hyper parameters
        rn = MLPRegressor()

        parameter_space = {
                'hidden_layer_sizes': [(i,) for i in list(range(1, 21))],
                'activation': ['tanh', 'relu'],
                'solver': 'adam', 
                'alpha': [0.0001, 0.05],
                'learning_rate': ['constant', 'adaptive'],
            }

        search = GridSearchCV(rn, parameter_space, n_jobs=-1, cv=5)

        search.fit(X_train_scale,y_train)
        clf = search.best_estimator_
        pred= search.predict(X_test_scale)

        cd = search.score(X_test_scale, y_test)

        valor_novo = features.tail(1)
        valor_novo

        previsao=scaler.transform(valor_novo)

        pred=lr.predict(previsao)

        df = df[df['Ativo'] == '' ]

        data_pregao_full=df['Data']
        data_pregao=data_pregao_full.tail(1)

        res_full=df['Fechamento']
        res=res_full.tail(1)

        # teste = Data  = data do proximo pregrao
        df=pd.DataFrame({'Data':'teste', 'real':res, 'previsao':pred})
        df.set_index('Data', inplace=True)

        return df

    def main(self):
        combined_df = self.read_and_preprocess_data(self.path)
        # Treinamento e previsão dos modelos
        lr_r2 = self.train_and_predict_models(combined_df)

        print(f"R² Score (Regressão Linear): {lr_r2}")

    

