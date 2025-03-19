from flask import Flask
from flask_cors import CORS
from config.db import get_database_uri,db
app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = get_database_uri()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

@app.route("/ping")
def ping():
    return "Server is running!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010, debug=True)
