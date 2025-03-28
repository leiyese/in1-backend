from config.db import db
from app import app
from models.subscription_models import Subscriptions_type, Subscription
from models.user import User



def reseed_db():
            
            # Remove all existing entries in the proper order to avoid foreign key issues
            User.query.delete()
            Subscription.query.delete()
            Subscriptions_type.query.delete()
            db.session.commit()

            # Seed default subscription types
            basic = Subscriptions_type(type="Basic", price=9.99)
            premium = Subscriptions_type(type="Premium", price=19.99)
            db.session.add_all([basic, premium])
            db.session.commit()

            # Create a test subscription using the basic subscription type


            # Create a user with the test subscription
            user = User(username="anton", email="test", password_hash="test")
            db.session.add(user)
            db.session.commit()

            print("Database seeded successfully!")


if __name__ == "__main__":
        with app.app_context():
                reseed_db()