import pandas as pd
import requests
from flask import request, render_template, app

from repository import depot_repository
from repository.depot_repository import DepotRepository
from service.api_service import get_coin_overview
from service.db_service import DbService
from service.environment_service import get_environment_variable
from service.gecko_service import GeckoService


class RoutingService():
    def __init__(self):
        self.db_service = DbService()
        self.depot_repository = DepotRepository(self.db_service.db)

    def coin_overview(self) -> str:
        crypto_asset_data = get_coin_overview()
        return render_template(
            template_name_or_list='overview/overview.html',
            title="Coin Overview",
            description="A list of crypto currencies:",
            crypto_asset_data=crypto_asset_data
        )

    def search_depot(self) -> str:
        return render_template(template_name_or_list='depot/depot_search.html', title="Depot Search", )

    def get_depot(self) -> str:
        depot_id = request.form['depot_id']
        depot = depot_repository.get_depot_by_depot_id(depot_id=depot_id)
        if depot.get('depot_id') is not None:
            return render_template(template_name_or_list='depot/depot_overview.html', title="Depot Overview",
                                   depot=depot)
        else:
            return f'No Depot found with id: {depot_id}'

    def spotify(self) -> str:
        """
        data from https://www.kaggle.com/datasets/muhmores/spotify-top-100-songs-of-20152019
        An example to return a df as html table
        :return: a df as table
        """
        df = pd.read_csv(filepath_or_buffer='/Users/simon/PycharmProjects/sp_group_work/unit_tests/data/Spotify.csv')
        return render_template('spotify/spotify.html', tables=[df.to_html(classes='data')], titles=df.columns.values)

    def crypto(self) -> str:
        currencies = ['bitcoin', 'ethereum', 'litecoin']
        last_days = list(range(2, 31))
        return render_template(template_name_or_list='crypto/crypto.html', currencies=currencies, last_days=last_days)

    def crypto_result(self) -> str:
        gecko_service = GeckoService()
        currency = request.form.get('currency_select')
        last_days = request.form.get('last_days_select')
        crypto_graph = gecko_service.get_bitcoin_data(currency=currency, last_days=last_days)
        return render_template(template_name_or_list='crypto/crypto_result.html', graph=crypto_graph)

    def fomo(self) -> str:
        FOMO_API_KEY = get_environment_variable(key="FOMO_API_KEY")
        BASE_URL = 'https://tokenfomo.io/api/tokens/'
        blockchain = 'eth'

        url = f'{BASE_URL}{blockchain}?limit=10&apikey={FOMO_API_KEY}'

        response = requests.get(url=url)
        response_json = response.json()

        self.db_service.db["crypto"].insert_many(response_json)

        print(response_json)

        return render_template(
            template_name_or_list='fomo/fomo_test.html',
            title="Fomo",
            description="Last 7 days of FOMO data have been written to the db!",
        )

    def not_found(self, error) -> tuple[str, int]:
        print(error)
        return render_template(template_name_or_list='404.html'), 404
