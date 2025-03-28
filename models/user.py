from config.db import db
from models.subscription_models import Subscription

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # Relationship to access subscriptions
    subscriptions = db.relationship('Subscription', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"
