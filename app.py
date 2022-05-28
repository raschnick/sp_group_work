from flask import Flask, render_template, request

from service import routing_service

app = Flask(__name__)
# Load Configurations
app.config.from_object('config')


@app.route('/')
def home() -> str:
    return render_template(template_name_or_list='index.html')


@app.route('/crypto', methods=['GET'])
def crypto() -> str:
    return routing_service.crypto()


@app.route('/crypto_result', methods=['POST'])
def crypto_result() -> str:
    return routing_service.crypto_result()


@app.route('/fomo')
def fomo() -> str:
    blockchain = request.args.get('bc')
    search = request.args.get('search')

    return routing_service.fomo(search, blockchain)


@app.errorhandler(404)
def not_found(error) -> tuple[str, int]:
    return routing_service.not_found(error)


if __name__ == '__main__':
    app.run()
