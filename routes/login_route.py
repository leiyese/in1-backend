from flask import Blueprint, request, jsonify
from controllers.login_controller import authenticate

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/login", methods=["POST"])
def login():
    
    data = request.get_json()
    # Error messages specify type of error
    # Check if username and password has been provided
    if not data or "username" not in data or "password" not in data:
        return jsonify({"Error": "Missing username or password!"}), 400
    
    user_data, error = authenticate(data["username"], data["password"])
    
    if error:
        return jsonify({"Error": error}), 400
    
    # User_data contains: id, username, access_token
    return jsonify(user_data), 200