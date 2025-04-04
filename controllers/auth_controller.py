from models.user import User
from werkzeug.security import check_password_hash
from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token

def authenticate_user(username, password):
    # Return values is either data or error
    # Check if username and password are provided
    if not username or not password:
        return None, "Missing username or password!"
    
    # Check if user exists
    user = User.query.filter_by(username=username).first()
    if not user:
        return None, "User does not exist!"
    
    # Check if password is correct
    if not check_password_hash(user.password_hash, password):
        return None, "Incorrect password!"
    
    # If the login is successful, create access token
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    
    return access_token, refresh_token