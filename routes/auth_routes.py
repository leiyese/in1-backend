from flask import Blueprint, request, jsonify
from controllers.auth_controller import authenticate_user, validate_access_token

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/login", methods=["POST"])
def login():
    
    data = request.get_json()
    # Error messages specify type of error
    # Check if username and password has been provided
    if not data or "username" not in data or "password" not in data:
        return jsonify({"Error": "Missing username or password!"}), 400
    
    user_data, error = authenticate_user(data["username"], data["password"])
    
    if error:
        return jsonify({"Error": error}), 400
    
    # User_data contains: id, username, access_token
    return jsonify(user_data), 200

@auth_routes.route("/validate_token", methods=["POST"])
def validate_token():
    
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"Error": "No token provided!"}), 400
    
    success, error = validate_access_token(token)
    
    if error:
        return jsonify({"Error": error}), 400
    
    return jsonify({"Success": success}), 200