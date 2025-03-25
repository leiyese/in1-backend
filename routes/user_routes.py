from flask import Blueprint, request, jsonify
from controllers.user_controller import get_all_users, get_user_by_id, create_user, update_user, delete_user


user_routes = Blueprint("user_routes", __name__)

@user_routes.route("/", methods=["GET"])
def get_users():
    users, error = get_all_users()
    
    if error:
        return jsonify({"Error": error}), 400
    
    return jsonify({"users": users}), 200

@user_routes.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user, error = get_user_by_id(user_id)
    
    if error:
        return jsonify({"Error": error}), 400
    
    return jsonify({"user_id": user.id, "username": user.username, "email": user.email, "subscription_id": user.subscription_id}), 200

@user_routes.route("/create", methods=["POST"])
def create_user_route():
    
    data = request.get_json()
    
    new_user, error = create_user(data["username"], data["password_hash"], data["email"], data["subscription_id"])
    print(new_user, "Created!")
    
    if error:
        return jsonify({"Error": error}), 400
    
    return f"Successfully created user!{new_user.username}", 200

@user_routes.route("/update/<int:user_id>", methods=["PUT"])
def update_user_route(user_id):
    
    update_data = request.get_json()
    
    status, error = update_user(user_id, update_data)
    
    if error:
        return jsonify({"Error": error}), 400
    
    return jsonify({"Status": status}), 200

@user_routes.route("/delete/<int:user_id>", methods=["DELETE"])
def delete_user_route(user_id):
    
    data = request.get_json()
    
    status, error = delete_user(user_id, data["password"])
    
    if error:
        return jsonify({"Error": error}), 400
    
    return jsonify({"Status": status}), 200
