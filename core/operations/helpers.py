import requests
from core.models import APIConnections, AssetsType, Assets


def get_site(pk):
    return APIConnections.objects.get(id=int(pk))

def get_assets(id_list):
    return Assets.objects.filter(id__in=id_list)

def get_asset_type(id_list):
    return AssetsType.objects.filter(id__in=id_list)

def get_content_api(url):
    response = requests.get(url)
    return response.json()

# def get_bitcoin_price_history():
#     features = [
#         data['market_data']['current_price']['usd'],
#         data['market_data']['high_24h']['usd'],
#         data['market_data']['low_24h']['usd'],
#         data['market_data']['total_volume']['usd'],
#         data['market_data']['market_cap']['usd'],
#         # data['market_data']['price_change_percentage_5d'],
#         # data['market_data']['price_change_percentage_21d']
#         ]
    
#     labels = ['preco_abertura', 'preco_max', 'preco_minimo', 'volume_negocios', 'market_cap', 'mm5d', 'mm21d']

#     k_best_features = SelectKBest(k='all')
#     k_best_features.fit_transform([features], labels)
#     k_best_features_scores = k_best_features.scores
#     k_best_features_final = dict(zip(labels, k_best_features_scores))
#     print('Melhores features:')
#     for feature, score in k_best_features_final.items():
#         print(f'{feature}: {score}')

#     #df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
#     #return df
#     return features