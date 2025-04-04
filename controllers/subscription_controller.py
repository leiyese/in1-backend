from config.db import db
from models.subscription_models import Subscription, Subscriptions_type
from datetime import datetime, time
from models.user import User

def get_all_subscriptions():
    return Subscription.query.all()

def create_subscription(data):
    today = datetime.combine(datetime.now().date(), time())
    
    existing_subscription = Subscription.query.filter_by(user_id=data['user_id']).first()
    
    if existing_subscription:
        existing_subscription.subscriptions_type_id = data['subscriptions_type_id']
        db.session.commit()
        return existing_subscription, None
    else:
        new_subscription = Subscription(
            date=data.get('date', today),
            subscriptions_type_id=data['subscriptions_type_id'],
            user_id=data['user_id']
        )
        db.session.add(new_subscription)
        db.session.commit()
        return new_subscription, None

def update_subscription(subscription, data):
    subscription.subscriptions_type_id = data['subscriptions_type_id']
    db.session.commit()
    return subscription

def delete_subscription(subscription):
    user = User.query.filter_by(subscription_id=subscription.id).first()
    
    if user:
        user.subscription_id = None
        
    db.session.delete(subscription)
    db.session.commit()
    
    return {
        "id": subscription.id,
        "message": "Subscription successfully cancelled"
    }

def get_subscription_by_id(subscription_id):
    return db.session.get(Subscription, subscription_id)

def get_all_subscription_types():
    return Subscriptions_type.query.all()

def get_subscription_type_by_id(subscription_type_id):
    return db.session.get(Subscriptions_type, subscription_type_id)

def create_subscription_type(data):
    try:
        new_subscription_type = Subscriptions_type(
            type=data['type'],
            price=data['price']
        )
        db.session.add(new_subscription_type)
        db.session.commit()
        return new_subscription_type, None
    except Exception as e:
        return None, str(e)

def update_subscription_type(subscription_type, data):
    subscription_type.type = data['type']
    subscription_type.price = data['price']
    db.session.commit()
    return subscription_type

def delete_subscription_type(subscription_type):
    db.session.delete(subscription_type)
    db.session.commit()
    return subscription_type

def create_subscription_and_update_user(data):
    existing_subscription = Subscription.query.filter_by(user_id=data['user_id']).first()
    
    if existing_subscription:
        existing_subscription.subscriptions_type_id = data['subscriptions_type_id']
        db.session.commit()
        
        user = db.session.get(User, data['user_id'])
        if user:
            user.subscription_id = existing_subscription.id
            db.session.commit()
            
        return existing_subscription, None
    else:
        today = datetime.combine(datetime.now().date(), time())
        new_subscription = Subscription(
            date=data.get('date', today),
            subscriptions_type_id=data['subscriptions_type_id'],
            user_id=data['user_id']
        )
        db.session.add(new_subscription)
        db.session.commit()
        
        user_id = data['user_id']
        user = db.session.get(User, user_id)
        if user:
            user.subscription_id = new_subscription.id
            db.session.commit()
            
        return new_subscription, None