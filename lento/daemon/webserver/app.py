from flask import Flask

app = Flask(__name__)


@app.route("/")
def main():
    return "<h1>You tried to access a blocked site!</h1>"


if __name__ == "__main__":
    app.run(port=65531)
