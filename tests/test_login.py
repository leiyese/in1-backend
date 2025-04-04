import pytest
from app import app, db
from models.user import User
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv

# Ladda miljövariabler
load_dotenv()

@pytest.fixture
def client():
    # Sätt testläge
    app.config["TESTING"] = True
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    
    with app.app_context():
        # Skapa en testanvändare
        test_user = User(
            username="testuser",
            email="test@example.com",
            password_hash=generate_password_hash("testpassword")
        )
        db.session.add(test_user)
        db.session.commit()
        
        yield app.test_client()
        
        # Städa upp efter testet
        db.session.query(User).filter(User.username == "testuser").delete()
        db.session.commit()

def test_login_success(client):
    # Skicka POST-anrop till login-routen
    response = client.post("/authenticate/login", json={
        "username": "testuser",
        "password": "testpassword"
    })
    
    # Kontrollera att svaret är korrekt
    assert response.status_code == 200
    assert response.json == {"login": True}
    
    # Kontrollera att cookies sätts
    cookies = response.headers.get_all("Set-Cookie")
    assert any("access_token_cookie" in cookie for cookie in cookies)
    assert any("refresh_token_cookie" in cookie for cookie in cookies) 