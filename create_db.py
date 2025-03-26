from app import app, db

# Import additional models as needed

with app.app_context():
    db.create_all()
    print("Database created!")
