from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/ping")
def ping():
    return "Server is running!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010, debug=True)
