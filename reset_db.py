from app import app, db
from sqlalchemy import text

# Script to reset the database, useful when big changes to db models are made
with app.app_context():
    # Disable foreign key checks
    db.session.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
    
    # Drop all tables without checking foreign keys
    try:
        # Get all table names
        inspector = db.inspect(db.engine)
        table_names = inspector.get_table_names()
        
        # Drop each table
        for table in table_names:
            db.session.execute(text(f"DROP TABLE IF EXISTS {table}"))
        
        db.session.commit()
    except Exception as e:
        print(f"Error dropping tables: {e}")
        db.session.rollback()
    
    # Re-enable foreign key checks
    db.session.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
    
    # Recreate all tables
    db.create_all()
    print("Database reset successfully!")