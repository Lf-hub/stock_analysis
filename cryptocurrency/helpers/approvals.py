def is_approved_by_sma(sma_short, sma_long, current_price):
    if sma_short.iloc[-1] > sma_long.iloc[-1] and current_price > sma_short.iloc[-1]:
        return "É um bom momento para comprar."
    elif sma_short.iloc[-1] < sma_long.iloc[-1] and current_price < sma_short.iloc[-1]:
        return "É um bom momento para vender."
    else:
        return "Na dúvida."

def is_approved_by_rsi(rsi, current_price):
    if rsi.iloc[-1] > 70:
        return "É um bom momento para vender."
    elif rsi.iloc[-1] < 30:
        return "É um bom momento para comprar."
    else:
        return "Na dúvida."

def is_approved_by_bollinger_bands(upper_band, lower_band, current_price):
    if current_price > upper_band.iloc[-1]:
        return "É um bom momento para vender (sobre as bandas superiores)."
    elif current_price < lower_band.iloc[-1]:
        return "É um bom momento para comprar (abaixo das bandas inferiores)."
    else:
        return "Na dúvida."

def pair_trading():
    pass

def distortion():
    pass

def cointegration():
    pass
