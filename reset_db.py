from app import app, db
from sqlalchemy import text



# Script to reset the database, useful when big changes to db models are made
with app.app_context():
    # Disable foreign key checks
    db.session.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
    
    # Drop all tables
    db.drop_all()
    
    # Re-enable foreign key checks
    db.session.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
    
    # Recreate all tables
    db.create_all()
    print("Database reset successfully!")