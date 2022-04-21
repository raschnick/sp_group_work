import base64
from io import BytesIO

from matplotlib.figure import Figure

from flask import Flask, render_template, request, redirect, url_for, Response

from repository.depot_repository import DepotRepository
from service.api_service import get_coin_overview
from service.db_service import DbService

import pandas as pd

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
    return render_template('spotify/spotify.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)


@app.route('/graph')
def graph() -> str:
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 2])
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"

@app.errorhandler(404)
def not_found(error) -> tuple[str, int]:
    print(error)
    return render_template(template_name_or_list='404.html'), 404


if __name__ == '__main__':
    app.run()
