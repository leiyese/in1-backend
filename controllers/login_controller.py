from models.user import User
from werkzeug.security import check_password_hash
from flask import jsonify
from flask_jwt_extended import create_access_token

def authenticate(username, password):
    # Return values is either data or error
    # Check if username and password are provided
    if not username or not password:
        return None, "Missing username or password!"
    
    # Check if user exists
    user = User.query.filter_by(username=username).first()
    if not user:
        return None, "User does not exist!"
    
    # Check if password is correct
    if not check_password_hash(user.password, password):
        return None, "Incorrect password!"
    
    # If the login is successful, create access token
    access_token = create_access_token(identity=user.id)
    return {"id": user.id, "username": user.username, "access_token": access_token}, None