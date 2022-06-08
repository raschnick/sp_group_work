import base64
from datetime import datetime
from io import BytesIO

import matplotlib.ticker
from pycoingecko import CoinGeckoAPI
import matplotlib.pyplot as plt


class GeckoService:
    def __init__(self):
        # https://www.coingecko.com/api/documentations/v3#/
        self.cg_api = CoinGeckoAPI()
        self.vs_currency = 'usd'

    def get_coin_ids(self) -> [str]:
        coins = self.cg_api.get_coins()
        coin_ids = [x.get('id') for x in coins]
        coin_ids.sort()
        return coin_ids

    def get_reference_graph_as_str_buffer(self, last_days=7):
        return self.get_crypto_data_as_str_buffer(currency='bitcoin', last_days=last_days)

    def get_crypto_data_as_str_buffer(self, currency='bitcoin', last_days=7) -> str:
        currency_prices = self.load_currency_prices(currency_name=currency, last_days=last_days)
        graph = self.dict_to_graph_as_str_buffer(currency=currency, price_dict=currency_prices)
        return graph

    def load_currency_prices(self, currency_name: str, last_days: int) -> dict:
        data = self.cg_api.get_coin_market_chart_by_id(id=currency_name, vs_currency=self.vs_currency, days=last_days,
                                                       interval='daily')
        return data.get('prices')

    def dict_to_graph_as_str_buffer(self, currency: str, price_dict: dict) -> str:
        prices = list(map(lambda x: [datetime.fromtimestamp(x[0] / 1_000).strftime('%d.%m %H'), x[1]], price_dict))
        x_axis = list(map(lambda x: x[0], prices))
        y_axis = list(map(lambda x: x[1], prices))

        self.clear_plot()

        plt.plot(x_axis, y_axis, label=currency.capitalize())

        plt.xlabel('Timestamp')
        plt.ylabel(f'value in {self.vs_currency.upper()}')

        plt.xticks(ticks=[x_axis[0], x_axis[int(len(x_axis) / 2)], x_axis[len(x_axis) - 1]])
        plt.legend()

        buf = BytesIO()
        plt.savefig(buf, format="png")
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return data

    def clear_plot(self):
        fig = plt.figure()
        plt.figure().clear()
        plt.close()
        plt.cla()
        plt.clf()
