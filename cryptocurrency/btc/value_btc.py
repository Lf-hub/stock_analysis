import requests
import pandas as pd


def get_bitcoin_price_history():
    # Use uma API de sua escolha para obter o histórico de preços do Bitcoin.
    # Neste exemplo, usaremos a API da CoinGecko.
    url = "https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=usd&days=365"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
    return df

def calculate_sma(data, window):
    return data['price'].rolling(window=window).mean()

def analyze_bitcoin():
    # Obtenha o histórico de preços do Bitcoin.
    bitcoin_price_history = get_bitcoin_price_history()

    # Calcule as médias móveis simples.
    sma_short_term = calculate_sma(bitcoin_price_history, window=50)
    sma_long_term = calculate_sma(bitcoin_price_history, window=200)

    # Obtenha o preço atual do Bitcoin.
    current_price = bitcoin_price_history['price'].iloc[-1]

    # Determine se é um bom momento para comprar ou vender.
    trade_decision = is_good_time_to_trade(sma_short_term, sma_long_term, current_price)

    print("Preço atual do Bitcoin: $", current_price)
    print(trade_decision)

def is_good_time_to_trade(sma_short, sma_long, current_price):
        if sma_short.iloc[-1] > sma_long.iloc[-1] and current_price > sma_short.iloc[-1]:
            return "É um bom momento para comprar."
        elif sma_short.iloc[-1] < sma_long.iloc[-1] and current_price < sma_short.iloc[-1]:
            return "É um bom momento para vender."
        else:
            return "A situação não está clara. Aguarde."