from config.db import db

#initial structure of the Subscription model

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, nullable=False)
    subscriptions_type_id = db.Column(db.Integer, db.ForeignKey('subscriptions_types.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"<Subscription {self.id}>"
    
    def serialize(self):
        return {
            "id": self.id,
            "date": self.date,
            "subscriptions_type_id": self.subscriptions_type_id
        }

class Subscriptions_type(db.Model):
    __tablename__ = 'subscriptions_types'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Subscription type {self.type}>"

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "price": self.price
        }