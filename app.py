from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
from config.db import get_database_uri, db
from routes.auth_routes import auth_routes
from routes.subscription_routes import subscription_routes
from routes.user_routes import user_routes
from routes.ai_api_routes import ai_api_routes
import os

app = Flask(__name__)
CORS(app)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "mysecretkey")
app.config["SQLALCHEMY_DATABASE_URI"] = get_database_uri()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "myjwtsecret")
app.config["JWT_COOKIE_CSRF_PROTECT"] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth_routes, url_prefix="/authenticate")
app.register_blueprint(user_routes, url_prefix="/users")
app.register_blueprint(ai_api_routes, url_prefix="/ai")
app.register_blueprint(subscription_routes, url_prefix="/subscriptions")


@app.route("/ping")
def ping():
    return "Server is running!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010, debug=True)