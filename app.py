from flask import Flask
from flask_cors import CORS
# from config.db import get_database_uri, db
from routes.ai_api_routes import ai_api_routes
app = Flask(__name__)
CORS(app)

# app.config["SQLALCHEMY_DATABASE_URI"] = get_database_uri()
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db.init_app(app)

app.register_blueprint(ai_api_routes,  url_prefix='/api')

@app.route("/ping")
def ping():
    return "Server is running!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010, debug=True)