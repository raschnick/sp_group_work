from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, can someone here me? I am stuck in a container!'


if __name__ == '__main__':
    app.run(debug=True)
