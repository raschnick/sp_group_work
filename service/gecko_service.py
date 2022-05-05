import base64
from datetime import datetime
from io import BytesIO

from pycoingecko import CoinGeckoAPI
import matplotlib.pyplot as plt


class GeckoService:
    def __init__(self):
        # https://www.coingecko.com/api/documentations/v3#/
        self.cg_api = CoinGeckoAPI()
        self.vs_currency = 'usd'

    def get_bitcoin_data_as_str_buffer(self, currency='bitcoin', last_days=7) -> str:
        bitcoin_prices = self.load_bitcoin_prices(currency_name=currency, last_days=last_days)
        graph = self.dict_to_graph_as_str_buffer(bitcoin_prices)
        return graph

    def load_bitcoin_prices(self, currency_name: str, last_days: int) -> dict:
        data = self.cg_api.get_coin_market_chart_by_id(id=currency_name, vs_currency=self.vs_currency, days=last_days,
                                                       intervall='daily')
        return data.get('prices')

    def dict_to_graph_as_str_buffer(self, price_dict: dict) -> str:
        prices = list(map(lambda x: [datetime.fromtimestamp(x[0] / 1_000).strftime('%d.%m %H:%M'), x[1]], price_dict))
        x_axis = list(map(lambda x: x[0], prices))
        y_axis = list(map(lambda x: x[1], prices))

        fig, ax = plt.subplots()
        # set max amount of minor tick labels
        ax.xaxis.set_major_locator(plt.MaxNLocator(3))
        ax.plot(x_axis, y_axis, linewidth=2.0)
        plt.xlabel('currency')
        plt.ylabel(f'value in {self.vs_currency.upper()}')

        buf = BytesIO()
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return data