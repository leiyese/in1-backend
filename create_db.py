from app import app, db
from models.User import User
from models.Corporation import Corporation
from models.Prompthistory import Prompthistory
# Import additional models as needed

with app.app_context():
    db.create_all()
    print("Database created!")
