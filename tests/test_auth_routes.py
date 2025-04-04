import pytest
from werkzeug.security import generate_password_hash
from app import app as flask_app
from models.user import User
from config.db import db

@pytest.fixture
def app():

    flask_app.config.update({
        "TESTING": True,
        "JWT_COOKIE_CSRF_PROTECT": False,
        "JWT_SECRET_KEY": "test-secret-key",
    })
    
    with flask_app.app_context():

        db.session.query(User).filter(User.username == 'testuser').delete()
        db.session.commit()
        
        hashed_password = generate_password_hash('testpassword')
        test_user = User(
            username='testuser', 
            email='test@example.com', 
            password_hash=hashed_password
        )
        db.session.add(test_user)
        db.session.commit()
    
    yield flask_app
    
    with flask_app.app_context():
        db.session.query(User).filter(User.username == 'testuser').delete()
        db.session.commit()

@pytest.fixture
def client(app):

    return app.test_client()

@pytest.fixture
def authenticated_client(client):

    login_data = {
        'username': 'testuser',
        'password': 'testpassword'
    }
    response = client.post('/authenticate/login', json=login_data)
    assert response.status_code == 200
    return client

def test_login(client):

    login_response = client.post('/authenticate/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })

    assert login_response.status_code == 200
    assert login_response.json == {'login': True}

    cookies = login_response.headers.get_all('Set-Cookie')
    assert any('access_token_cookie' in cookie for cookie in cookies)
    assert any('refresh_token_cookie' in cookie for cookie in cookies)

def test_logout(authenticated_client):

    logout_response = authenticated_client.post('/authenticate/logout')

    assert logout_response.status_code == 200
    assert logout_response.json == {'logout': True}

    logout_cookies = logout_response.headers.get_all('Set-Cookie')
    assert any('access_token_cookie=;' in cookie for cookie in logout_cookies)
    assert any('refresh_token_cookie=;' in cookie for cookie in logout_cookies)