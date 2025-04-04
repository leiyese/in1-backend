# tests/conftest.py
import pytest
from flask import Flask
import os

# Assume your blueprint is in controllers.ai_api_controller
# Adjust the import path if your structure is different
from routes.ai_api_routes import ai_api_routes


@pytest.fixture(scope="module")
def app():
    """Create and configure a new app instance for each test module."""
    # Set dummy environment variables for testing initialization if needed
    # We will often mock os.getenv directly in tests anyway
    os.environ["GEMINI_API_KEY"] = "test_gemini_key"
    os.environ["HF_API_KEY"] = "test_hf_key"

    flask_app = Flask(__name__)
    flask_app.config["TESTING"] = True
    flask_app.register_blueprint(ai_api_routes)

    # Clean up environment variables after tests if set here
    yield flask_app
    del os.environ["GEMINI_API_KEY"]
    del os.environ["HF_API_KEY"]


@pytest.fixture(scope="module")
def client(app):
    """A test client for the app."""
    return app.test_client()
