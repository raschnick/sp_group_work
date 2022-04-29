from flask import Flask, render_template, redirect, url_for, Response

from service.routing_service import RoutingService

app = Flask(__name__)
# Load Configurations
app.config.from_object('config')

routing_service_ = RoutingService()


@app.route('/')
def home() -> str:
    return render_template(template_name_or_list='index.html')


@app.route('/overview')
def coin_overview() -> str:
    return routing_service_.coin_overview()


@app.route('/depot')
def hello() -> Response:
    return redirect(url_for(endpoint='search_depot'))


@app.route('/depot/search', methods=['GET'])
def search_depot() -> str:
    return routing_service_.search_depot()


@app.route('/depot/overview', methods=['POST'])
def get_depot() -> str:
    return routing_service_.get_depot()


@app.route('/spotify')
def spotify() -> str:
    return routing_service_.spotify()


@app.route('/crypto', methods=['GET'])
def crypto() -> str:
    return routing_service_.crypto()


@app.route('/crypto_result', methods=['POST'])
def crypto_result() -> str:
    return routing_service_.crypto_result()


@app.route('/fomo')
def fomo() -> str:
    return routing_service_.fomo()


@app.errorhandler(404)
def not_found(error) -> tuple[str, int]:
    return routing_service_.not_found(error)


if __name__ == '__main__':
    app.run()
