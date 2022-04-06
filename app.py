from flask import Flask, render_template, request

from repository.depot_repository import DepotRepository
from service.db_service import DbService
import json
import os

import requests

app = Flask(__name__)
# Load Configurations
app.config.from_object('config')

db_service = DbService()
depot_repository = DepotRepository(db_service.db)


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


@app.route('/depot/search', methods=['GET'])
def search_depot():
    return render_template('depot/depot_search.html')


@app.route('/depot/overview', methods=['POST'])
def get_depot():
    depot_id = request.form['depot_id']
    depot = depot_repository.get_depot_by_depot_id(depot_id)
    if depot.get('depot_id') is not None:
        return render_template('depot/depot_overview.html', depot=depot)
    else:
        return f'No Depot found with id: {depot_id}'


@app.errorhandler(404)
def not_found(error):
    print(error)
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
