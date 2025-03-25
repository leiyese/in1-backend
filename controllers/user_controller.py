from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User


def get_all_users():
    
    try:
        users = User.query.all()
        return users, None
    except Exception as e:
        return None, e
    
def get_user_by_id(user_id):
    
    try:
        user = User.query.filter_by(id=user_id).first()
        return user, None
    except Exception as e:
        return None, e
    
def create_user(username, password):
    
    users = get_all_users()
    
    if not username or not password:
        return None, "Missing username or password!"
    
    if username in [user.username for user in users]:
        return None, "Username already exists!"
    
    new_user = User(username=username, password=generate_password_hash(password))
    
    return new_user, None

def update_user(user_id, update_data):
    
    user = get_user_by_id(user_id)
    
    if not user:
        return None, "User does not exist!"
    
    try:
        if "username" in update_data:
            user.username = update_data["username"]
        if "password" in update_data:
            user.password = generate_password_hash(update_data["password"])
        if "email" in update_data:
            user.email = update_data["email"]
        return "status: success", None
    except Exception as e:
        return None, e
    
def delete_user(user_id, password):
    
    user = get_user_by_id(user_id)
    
    if not user:
        return None, "User does not exist!"
    if not password:
        return None, "Missing password!"
    if not check_password_hash(user.password_hash, password):
        return None, "Incorrect password!"
    
    try:
        User.query.filter_by(id=user_id).delete()
        return "status: successfully deleted user.", None
    except Exception as e:
        return None, e