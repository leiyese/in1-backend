from flask import Blueprint, request, jsonify
from controllers.auth_controller import authenticate_user
from flask_jwt_extended import (jwt_required, get_jwt_identity, set_access_cookies,
                                set_refresh_cookies, create_access_token,
                                unset_jwt_cookies)
from models.user import User

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/login", methods=["POST"])
def login():
    
    data = request.get_json()
    # Error messages specify type of error
    # Check if username and password has been provided
    if not data or "username" not in data or "password" not in data:
        return jsonify({"Error": "Missing username or password!"}), 400
    
    access_token, refresh_token = authenticate_user(data["username"], data["password"])
    
    resp = jsonify({"login": True})
    print("login successful")
    
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    print("cookies set")
    
    return resp, 200

@auth_routes.route("/logout", methods=["POST"])
def logout():
    resp = jsonify({"logout": True})
    unset_jwt_cookies(resp)
    return resp, 200

@auth_routes.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=str(current_user.id))
    resp = jsonify({"refresh": True})
    set_access_cookies(resp, access_token)
    return resp, 200

@auth_routes.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    current_user = User.query.filter_by(id=current_user_id).first()
    return jsonify(logged_in_as=current_user_id, username=current_user.username, email=current_user.email), 200