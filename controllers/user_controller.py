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
    
def create_user(username, password, email, subscription_id):
    
    if not username or not password:
        return None, "Missing username or password!"
    
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return None, "User already exists!"
    
    new_user = User(username=username, password_hash=generate_password_hash(password), email=email, subscription_id=subscription_id)
    
    db.session.add(new_user)
    db.session.commit()
    
    return new_user, None

def update_user(user_id, update_data):
    
    user, error = get_user_by_id(user_id)
    
    if error:
        return None, error
    if not user:
        return None, "User does not exist!"
    
    try:
        if "password" not in update_data:
            return None, "Missing password!"
        if not check_password_hash(user.password_hash, update_data["password"]):
            return None, "Incorrect password!"
        if "username" in update_data:
            user.username = update_data["username"]
        if "new_password" in update_data:
            user.password_hash = generate_password_hash(update_data["new_password"])
        if "email" in update_data:
            user.email = update_data["email"]
        
        db.session.commit()
        
        return "status: success", None
    except Exception as e:
        return None, e
    
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