import json

import requests

from service.environment_service import get_environment_variable


def get_coin_overview() -> dict:
    url = 'https://rest.coinapi.io/v1/assets'
    headers = {'X-CoinAPI-Key': get_environment_variable(key='API_KEY')}
    response = requests.get(url=url, headers=headers)
    asset_data = json.loads(s=response.text)

    crypto_asset_data = dict()

    for asset in asset_data:
        if asset.get('type_is_crypto') == 1:
            crypto_asset_data[asset.get('name')] = asset

    return crypto_asset_data
