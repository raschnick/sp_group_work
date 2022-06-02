from datetime import datetime

import pandas as pd
import requests
from flask import request, render_template

from service.environment_service import get_environment_variable
from service.gecko_service import GeckoService


def crypto() -> str:
    gecko_service = GeckoService()
    currencies = gecko_service.get_coin_ids()
    last_days = list(range(2, 31))
    return render_template(template_name_or_list='crypto/crypto.html', title="Check Coins", currencies=currencies, last_days=last_days)


def crypto_result() -> str:
    gecko_service = GeckoService()
    currency = request.form.get('currency_select')
    last_days = request.form.get('last_days_select')
    crypto_graph = gecko_service.get_bitcoin_data_as_str_buffer(currency=currency, last_days=last_days)
    return render_template(template_name_or_list='crypto/crypto_result.html', title="Check Coins", graph=crypto_graph)


def fomo(search, blockchain='eth') -> str:
    FOMO_API_KEY = get_environment_variable(key="FOMO_API_KEY")
    BASE_URL = 'https://tokenfomo.io/api/tokens/'

    url = f'{BASE_URL}{blockchain}?apikey={FOMO_API_KEY}'

    response = requests.get(url=url)

    fomo_data = response.json()

    filtered_fomo_data = []

    if not search is None:
        for element in fomo_data:
            if search in element.get('name'):
                filtered_fomo_data.append(element)

        contract_addresses = [addr.get('addr') for addr in filtered_fomo_data]
        names = [name.get('name') for name in filtered_fomo_data]
        symbols = [symbol.get('symbol') for symbol in filtered_fomo_data]
        timestamps = [timestamp.get('timestamp') for timestamp in filtered_fomo_data]
    else:
        contract_addresses = [addr.get('addr') for addr in fomo_data]
        names = [name.get('name') for name in fomo_data]
        symbols = [symbol.get('symbol') for symbol in fomo_data]
        timestamps = [timestamp.get('timestamp') for timestamp in fomo_data]

    timestamps_formatted = []

    for timestamp in timestamps:
        timestamps_formatted.append(datetime.fromtimestamp(int(timestamp)).strftime('%d.%m.%y'))

    df = pd.DataFrame({'Contract Address': contract_addresses,
                       'Name': names,
                       'Symbol': symbols,
                       'Timestamp': timestamps_formatted})

    return render_template('fomo/fomo.html', title="Check Tokens",
                           tables=[df.to_html(classes='table table-striped table-bordered fomo-table'), ],
                           titles=df.columns.values)


def not_found(error) -> tuple[str, int]:
    print(error)
    return render_template(template_name_or_list='404.html'), 404
