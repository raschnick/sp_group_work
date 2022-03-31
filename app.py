import json
import os

import requests

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template(
        'index.html'
    )

@app.route('/fluff')
def fluff():
    return render_template(
        'fluff.html'
    )

@app.route('/overview')
def coin_overview():
    url = 'https://rest.coinapi.io/v1/assets'
    headers = {'X-CoinAPI-Key': os.environ['API_KEY']}
    response = requests.get(url, headers=headers)
    asset_data = json.loads(response.text)

    crypto_asset_data = dict()

    for asset in asset_data:
        if(asset.get('type_is_crypto') == 1):
            crypto_asset_data[asset.get('name')] = asset


    return render_template(
        'overview.html',
        title="Coin Overview",
        description="A list of crypto currencies:",
        crypto_asset_data=crypto_asset_data
    )


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
