from datetime import datetime

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

    def crypto(self) -> str:
        currencies = ['bitcoin', 'ethereum', 'litecoin']
        last_days = list(range(2, 31))
        return render_template(template_name_or_list='crypto/crypto.html', currencies=currencies, last_days=last_days)

    def crypto_result(self) -> str:
        gecko_service = GeckoService()
        currency = request.form.get('currency_select')
        last_days = request.form.get('last_days_select')
        crypto_graph = gecko_service.get_bitcoin_data_as_str_buffer(currency=currency, last_days=last_days)
        return render_template(template_name_or_list='crypto/crypto_result.html', graph=crypto_graph)

    def fomo(self, blockchain) -> str:
        print("------------blockchain: " + blockchain)
        FOMO_API_KEY = get_environment_variable(key="FOMO_API_KEY")
        BASE_URL = 'https://tokenfomo.io/api/tokens/'

        url = f'{BASE_URL}{blockchain}?apikey={FOMO_API_KEY}'

        response = requests.get(url=url)

        fomo_data_json = response.json()

        contract_addresses = [addr.get('addr') for addr in fomo_data_json]
        names = [name.get('name') for name in fomo_data_json]
        symbols = [symbol.get('symbol') for symbol in fomo_data_json]
        timestamps = [timestamp.get('timestamp') for timestamp in fomo_data_json]
        timestamps_formatted = []

        print(f'normal length: {len(timestamps)}')
        print(f'formatted length: {len(timestamps_formatted)}')

        for timestamp in timestamps:
            timestamps_formatted.append(datetime.fromtimestamp(int(timestamp)).strftime('%d.%m.%y'))

        df = pd.DataFrame({'Contract Address': contract_addresses,
                           'Name': names,
                           'Symbol': symbols,
                           'Timestamp': timestamps_formatted})

        return render_template('fomo/fomo.html', title="Fomo",
                               tables=[df.to_html(classes='table table-striped table-bordered fomo-table')],
                               titles=df.columns.values)

    def not_found(self, error) -> tuple[str, int]:
        print(error)
        return render_template(template_name_or_list='404.html'), 404
