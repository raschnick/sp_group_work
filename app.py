from flask import Flask, render_template, request, redirect, url_for, Response
from repository.depot_repository import DepotRepository
from service.db_service import DbService
import json
import os
import requests

app = Flask(__name__)
# Load Configurations
app.config.from_object('config')

# global variables
db_service = DbService()
depot_repository = DepotRepository(db_service.db)


@app.route('/')
def home() -> str:
    return render_template(template_name_or_list='index.html')


@app.route('/fluff')
def fluff() -> str:
    return render_template(template_name_or_list='fluff/fluff.html')


@app.route('/overview')
def coin_overview() -> str:
    url = 'https://rest.coinapi.io/v1/assets'
    headers = {'X-CoinAPI-Key': os.environ['API_KEY']}
    response = requests.get(url=url, headers=headers)
    asset_data = json.loads(s=response.text)

    crypto_asset_data = dict()

    for asset in asset_data:
        if asset.get('type_is_crypto') == 1:
            crypto_asset_data[asset.get('name')] = asset

    return render_template(
        template_name_or_list='fluff/overview.html',
        title="Coin Overview",
        description="A list of crypto currencies:",
        crypto_asset_data=crypto_asset_data
    )


@app.route('/depot')
def hello() -> Response:
    return redirect(url_for(endpoint='search_depot'))


@app.route('/depot/search', methods=['GET'])
def search_depot() -> str:
    return render_template(template_name_or_list='depot/depot_search.html')


@app.route('/depot/overview', methods=['POST'])
def get_depot() -> str:
    depot_id = request.form['depot_id']
    depot = depot_repository.get_depot_by_depot_id(depot_id=depot_id)
    if depot.get('depot_id') is not None:
        return render_template(template_name_or_list='depot/depot_overview.html', depot=depot)
    else:
        return f'No Depot found with id: {depot_id}'


@app.errorhandler(404)
def not_found(error) -> tuple[str, int]:
    print(error)
    return render_template(template_name_or_list='404.html'), 404


if __name__ == '__main__':
    app.run()
