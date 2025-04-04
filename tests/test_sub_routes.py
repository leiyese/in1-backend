import pytest
from werkzeug.security import generate_password_hash
from app import app as flask_app
from models.user import User
from models.subscription_models import Subscription, Subscriptions_type
from config.db import db
from datetime import datetime


@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
        "JWT_COOKIE_CSRF_PROTECT": False,
        "JWT_SECRET_KEY": "test-secret-key",
    })
    
    with flask_app.app_context():
        try:
            User.query.filter_by(id=9999).update({"subscription_id": None})
            db.session.commit()
            
            Subscription.query.filter_by(user_id=9999).delete()
            User.query.filter_by(username='testsubuser').delete()
            Subscriptions_type.query.filter_by(type='Test Type').delete()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error during setup cleanup: {e}")
        
        try:
            test_user = User(
                id=9999,
                username='testsubuser', 
                email='testsub@example.com', 
                password_hash=generate_password_hash('testpassword')
            )
            db.session.add(test_user)
            
            test_sub_type = Subscriptions_type(
                type='Test Type',
                price=4.99
            )
            db.session.add(test_sub_type)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error setting up test data: {e}")
    
    yield flask_app
    
    with flask_app.app_context():
        try:
            User.query.filter_by(id=9999).update({"subscription_id": None})
            db.session.commit()
            
            Subscription.query.filter_by(user_id=9999).delete()
            User.query.filter_by(id=9999).delete()
            Subscriptions_type.query.filter_by(type='Test Type').delete()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error during teardown: {e}")


@pytest.fixture
def client(app):
    return app.test_client()


def test_create_subscription(client):
    with flask_app.app_context():
        sub_type = Subscriptions_type.query.filter_by(type='Test Type').first()
        
    response = client.post('/subscriptions/create_subscription', json={
        'user_id': 9999,
        'subscriptions_type_id': sub_type.id
    })
    
    assert response.status_code == 200
    assert response.json['message'] == "subscriptions created!"
    assert response.json['user_id'] == 9999
    
    with flask_app.app_context():
        sub = Subscription.query.filter_by(user_id=9999).first()
        assert sub is not None
        assert sub.subscriptions_type_id == sub_type.id


def test_get_subscriptions(client):
    with flask_app.app_context():
        sub_type = Subscriptions_type.query.filter_by(type='Test Type').first()
        
    client.post('/subscriptions/create_subscription', json={
        'user_id': 9999,
        'subscriptions_type_id': sub_type.id
    })
    
    response = client.get('/subscriptions/get_subscriptions')
    
    assert response.status_code == 200
    assert isinstance(response.json, list)
    
    found = False
    for sub in response.json:
        if sub['user_id'] == 9999:
            found = True
            break
    
    assert found == True


def test_get_subscription_types(client):
    response = client.get('/subscriptions/get_subscription_types')
    
    assert response.status_code == 200
    assert isinstance(response.json, list)
    
    found = False
    for sub_type in response.json:
        if sub_type['type'] == 'Test Type':
            found = True
            break
    
    assert found == True


def test_create_and_update_user_subscription(client):
    with flask_app.app_context():
        sub_type = Subscriptions_type.query.filter_by(type='Test Type').first()
        
    response = client.post('/subscriptions/create_subscription_and_update_user', json={
        'user_id': 9999,
        'subscriptions_type_id': sub_type.id
    })
    
    assert response.status_code == 201
    assert response.json['message'] == "Subscription created and user updated!"
    
    with flask_app.app_context():
        user = db.session.get(User, 9999)
        assert user.subscription_id is not None