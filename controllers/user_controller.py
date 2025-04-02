from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from config.db import db


def get_all_users():
    
    try:
        users = User.query.all()
        return [{"id": user.id, "username": user.username} for user in users], None
    except Exception as e:
        return None, e
    
def get_user_by_id(user_id):
    
    try:
        user = User.query.filter_by(id=user_id).first()
        return user, None
    except Exception as e:
        return None, e
    
def create_user(username, password, email, subscription_id=None):
    
    if not username or not password:
        return None, "Missing username or password!"
    
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return None, "User already exists!"
    
    new_user = User(username=username, password_hash=generate_password_hash(password), email=email)
    
    db.session.add(new_user)
    db.session.commit()
    
    return new_user, None

def update_user(user_id, update_data):
    print("Updating user with data:", update_data)  # Debug-utskrift
    
    if not update_data:
        return None, "No update data provided!"
    
    user, error = get_user_by_id(user_id)
    
    if error:
        print("Error getting user:", error)  # Debug-utskrift
        return None, error
    if not user:
        print("User not found")  # Debug-utskrift
        return None, "User does not exist!"
    
    try:
        # Uppdatera användarnamn om det finns
        if "username" in update_data:
            print("Updating username to:", update_data["username"])  # Debug-utskrift
            # Kontrollera om användarnamnet redan finns
            existing_user = User.query.filter_by(username=update_data["username"]).first()
            if existing_user and existing_user.id != user_id:
                return None, "Username already exists!"
            user.username = update_data["username"]
            
        # Uppdatera e-post om det finns
        if "email" in update_data:
            print("Updating email to:", update_data["email"])  # Debug-utskrift
            user.email = update_data["email"]
            
        # Om det finns andra fält i update_data som inte är username eller email, ignorera dem
        
        db.session.commit()
        print("Update successful")  # Debug-utskrift
        return "Profile updated successfully", None
    except Exception as e:
        db.session.rollback()
        print("Error updating user:", str(e))  # Debug-utskrift
        return None, str(e)
    
def delete_user(user_id, password):
    
    user, error = get_user_by_id(user_id)
    
    if error:
        return None, error
    
    if not user:
        return None, "User does not exist!"
    if not password:
        return None, "Missing password!"
    if not check_password_hash(user.password_hash, password):
        return None, "Incorrect password!"
    
    try:
        User.query.filter_by(id=user_id).delete()
        
        db.session.commit()
        
        return "successfully deleted user.", None
    except Exception as e:
        return None, e


def update_user_subscription(user_id, subscription_id): # New function to update user subscription, 
    user, error = get_user_by_id(user_id)
    if error:
        return None, error
    if not user:
        return None, "User does not exist!"
    
    try:
        user.subscription_id = subscription_id
        db.session.commit()
        return user, None
    except Exception as e:
        return None, str(e)