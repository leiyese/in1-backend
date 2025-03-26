from config.db import db
from models.subscription_models import Subscription, Subscriptions_type

def get_all_subscriptions():
    return Subscription.query.all()

def create_subscription(data):
    new_subscription = Subscription(
        date=data['date'],
        subscriptions_type_id=data['subscriptions_type_id']
    )
    db.session.add(new_subscription)
    db.session.commit()
    return new_subscription, None

def update_subscription(subscription, data):
    subscription.date = data['date']
    subscription.subscriptions_type_id = data['subscriptions_type_id']
    db.session.commit()
    return subscription

def delete_subscription(subscription):
    db.session.delete(subscription)
    db.session.commit()
    return subscription

def get_subscription_by_id(subscription_id):
    return Subscription.query.get(subscription_id)


#CRUD operations for the Subscriptions_type model

def get_all_subscription_types():
    return Subscriptions_type.query.all()

def get_subscription_type_by_id(subscription_type_id):
    return Subscriptions_type.query.get(subscription_type_id)

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