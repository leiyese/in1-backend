from config.db import db

#initial structure of the User model

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscriptions.id'), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    
    
    def __repr__(self):
        return f"<User {self.username}>"
