from config.db import db

#initial structure of the Subscription model

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, nullable=False)
    subscriptions_type_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Subscription {self.id}>"

class Subscriptions_type(db.Model):
    __tablename__ = 'subscriptions_types'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Integer, nullable=False) 
    price = db.Column(db.Float, nullable=False)
  
    
    def __repr__(self):
        return f"<Subscription type {self.name}>"