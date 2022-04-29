import base64
from io import BytesIO

import pandas as pd
import requests
from flask import Flask, render_template, request, redirect, url_for, Response
from matplotlib.figure import Figure

from repository.depot_repository import DepotRepository
from service.api_service import get_coin_overview
from service.db_service import DbService
from service.environment_service import get_environment_variable
from service.gecko_service import GeckoService

app = Flask(__name__)
# Load Configurations
app.config.from_object('config')

# global variables
db_service = DbService()
depot_repository = DepotRepository(db_service.db)


@app.route('/')
def home() -> str:
    return render_template(template_name_or_list='index.html')


@app.route('/overview')
def coin_overview() -> str:
    crypto_asset_data = get_coin_overview()
    return render_template(
        template_name_or_list='overview/overview.html',
        title="Coin Overview",
        description="A list of crypto currencies:",
        crypto_asset_data=crypto_asset_data
    )


@app.route('/depot')
def hello() -> Response:
    return redirect(url_for(endpoint='search_depot'))


@app.route('/depot/search', methods=['GET'])
def search_depot() -> str:
    return render_template(template_name_or_list='depot/depot_search.html', title="Depot Search", )


@app.route('/depot/overview', methods=['POST'])
def get_depot() -> str:
    depot_id = request.form['depot_id']
    depot = depot_repository.get_depot_by_depot_id(depot_id=depot_id)
    if depot.get('depot_id') is not None:
        return render_template(template_name_or_list='depot/depot_overview.html', title="Depot Overview", depot=depot)
    else:
        return f'No Depot found with id: {depot_id}'


@app.route('/spotify')
def spotify() -> str:
    """
    data from https://www.kaggle.com/datasets/muhmores/spotify-top-100-songs-of-20152019
    An example to return a df as html table
    :return: a df as table
    """
    df = pd.read_csv(filepath_or_buffer='/Users/simon/PycharmProjects/sp_group_work/unit_tests/data/Spotify.csv')
    return render_template('spotify/spotify.html', tables=[df.to_html(classes='data')], titles=df.columns.values)


@app.route('/gecko')
def pygecko() -> str:
    gecko_service = GeckoService()
    crypto_graph = gecko_service.get_bitcoin_data()
    return render_template(
        template_name_or_list='gecko/gecko_test.html',
        title="Gecko",
        description="First gecko example",
        graph=crypto_graph
    )


@app.route('/crypto', methods=['GET'])
def crypto() -> str:
    currencies = ['bitcoin', 'ethereum', 'litecoin']
    last_days = list(range(2, 31))
    return render_template(template_name_or_list='crypto/crypto.html', currencies=currencies, last_days=last_days)


@app.route('/crypto_result', methods=['POST'])
def crypto_result() -> str:
    gecko_service = GeckoService()
    currency = request.form.get('currency_select')
    last_days = request.form.get('last_days_select')
    crypto_graph = gecko_service.get_bitcoin_data(currency=currency, last_days=last_days)
    return render_template(template_name_or_list='crypto/crypto_result.html', graph=crypto_graph)


@app.route('/fomo')
def fomo() -> str:
    FOMO_API_KEY = get_environment_variable(key="FOMO_API_KEY")
    BASE_URL = 'https://tokenfomo.io/api/tokens/'
    blockchain = 'eth'

    url = f'{BASE_URL}{blockchain}?limit=10&apikey={FOMO_API_KEY}'

    response = requests.get(url=url)
    response_json = response.json()

    db_service.db["crypto"].insert_many(response_json)

    print(response_json)

    return render_template(
        template_name_or_list='fomo/fomo_test.html',
        title="Fomo",
        description="Last 7 days of FOMO data have been written to the db!",
    )


@app.errorhandler(404)
def not_found(error) -> tuple[str, int]:
    print(error)
    return render_template(template_name_or_list='404.html'), 404


if __name__ == '__main__':
    app.run()
