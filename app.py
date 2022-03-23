from flask import Flask, render_template

app = Flask(__name__)
# Load Configurations
app.config.from_object('config')


@app.route('/')
def hello_world():
    return 'Hello, can someone here me? I am stuck in a container!'


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
