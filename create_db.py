from app import app, db
from models.ai_models import AI_model, AI_type
from models.user import User
from models.subscription_models import Subscription, Subscription_type
from models.payment_models import Payment
from models.corporation import Corporation
from models.prompthistory import Prompthistory
# Import additional models as needed

with app.app_context():
    db.create_all()
    print("Database created!")
