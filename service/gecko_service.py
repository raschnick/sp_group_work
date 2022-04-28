import base64
from datetime import datetime
from io import BytesIO

from pycoingecko import CoinGeckoAPI
import matplotlib.pyplot as plt


def dict_to_graph_str(dictionary: dict) -> str:
    prices = list(map(lambda x: [datetime.fromtimestamp(x[0] / 1_000).strftime('%Y-%m-%d %H'), x[1]], dictionary))
    x_axis = list(map(lambda x: x[0], prices))
    y_axis = list(map(lambda x: x[1], prices))

    fig, ax = plt.subplots()
    ax.plot(x_axis, y_axis, linewidth=2.0)
    plt.xlabel('currency')
    plt.ylabel('value in $')

    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data


class GeckoService:
    def __init__(self):
        # https://www.coingecko.com/api/documentations/v3#/
        self.cg_api = CoinGeckoAPI()
        self.crypto_currencies = ['bitcoin', 'ethereum', 'litecoin']

    def load_currencies(self) -> None:
        bitcoin_price_in_usd = self.cg_api.get_price(ids=self.crypto_currencies, vs_currencies='usd',
                                                     include_market_cap='true', include_24hr_vol='true',
                                                     include_24hr_change='true', include_last_updated_at='true', )
        dict_to_graph_str(dictionary=bitcoin_price_in_usd)
        print('0-------------')
        print(bitcoin_price_in_usd)
        print('1-------------')
        print(datetime.fromtimestamp(bitcoin_price_in_usd.get("bitcoin").get("last_updated_at")))
        print('2-------------')
        historical_bitcoin_price = self.cg_api.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days='3')
        print(historical_bitcoin_price)
        print('3-------------')
        print(len(historical_bitcoin_price.get("prices")))
        print('4-------------')

        global_mc = self.cg_api.get_global(id='btc')
        print(global_mc)

    def get_bitcoin_data(self) -> str:
        bitcoin_prices = self.load_bitcoin_prices()
        graph = dict_to_graph_str(bitcoin_prices)
        return graph

    def load_bitcoin_prices(self) -> dict:
        data = self.cg_api.get_coin_market_chart_by_id(id='bitcoin', vs_currency='chf', days=7,
                                                         intervall='daily')
        return data.get('prices')
