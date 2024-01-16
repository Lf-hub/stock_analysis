import requests
import pandas as pd
from cryptocurrency.helpers import calculate, approvals


def get_bitcoin_price_history(code):
    # Use uma API de sua escolha para obter o histórico de preços do Bitcoin.
    # Neste exemplo, usaremos a API da CoinGecko.
    url = f"https://api.coingecko.com/api/v3/coins/{code}/market_chart?vs_currency=usd&days=365"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
    return df

def analyze_bitcoin(code):
    # Obtenha o histórico de preços do Bitcoin.
    try:
        bitcoin_price_history = get_bitcoin_price_history(code)

        # Calcule as médias móveis simples 50.
        sma_short_term = calculate.calculate_sma(bitcoin_price_history, window=50)
        # Calcule as médias móveis simples 200.
        sma_long_term = calculate.calculate_sma(bitcoin_price_history, window=200)

        # Calcule o RSI.
        rsi = calculate.calculate_rsi(bitcoin_price_history)

        # Calcule as Bandas de Bollinger.
        upper_band, lower_band = calculate.calculate_bollinger_bands(bitcoin_price_history)
        
        # Obtenha o preço atual do Bitcoin.
        current_price = bitcoin_price_history['price'].iloc[-1]
        
        # Avalie se a condição é aprovada por cada indicador.
        sma_result = approvals.is_approved_by_sma(sma_short_term, sma_long_term, current_price)
        rsi_result = approvals.is_approved_by_rsi(rsi, current_price)
        bollinger_result = approvals.is_approved_by_bollinger_bands(upper_band, lower_band, current_price)

        # Retorne as avaliações de cada indicador.
        return {
            "SMA": sma_result,
            "RSI": rsi_result,
            "Bollinger": bollinger_result
        }
    except:
        return {
            "SMA": 'Sem resultado',
            "RSI": 'Sem resultado',
            "Bollinger": 'Sem resultado'
        }