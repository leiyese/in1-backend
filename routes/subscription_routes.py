from flask import Blueprint, request, jsonify
from controllers.subscription_controller import *

subscription_routes = Blueprint("subscription_routes", __name__)


@subscription_routes.route("/create_subscription", methods=["POST"])
def create_subscription_route():
    
    data = request.get_json()
    
    new_subscription, error = create_subscription(data)
    
    if error:
        return jsonify ({"error":error}), 400
    return jsonify({
        "message": "subscriptions created!",
        "subscription_id": new_subscription.id,  # Fixed to use 'id'
        "date": new_subscription.date,
        "subscriptions_type_id": new_subscription.subscriptions_type_id  # Fixed key
    })
    
@subscription_routes.route("/get_subscriptions", methods=["GET"])
def get_all_subscriptions_route():
    
    subscriptions = get_all_subscriptions()
    
    return jsonify([subscription.serialize() for subscription in subscriptions])



@subscription_routes.route("/get_subscription/<subscription_id>", methods=["GET"])
def get_subscription_by_id_route(subscription_id):
    
    subscription = get_subscription_by_id(subscription_id)
    
    return jsonify(subscription.serialize())


@subscription_routes.route("/update_subscription/<subscription_id>", methods=["PUT"])
def update_subscription_route(subscription_id):
    
    data = request.get_json()
    
    subscription = get_subscription_by_id(subscription_id)
    updated_subscription = update_subscription(subscription, data)
    
    return jsonify(updated_subscription.serialize())


@subscription_routes.route("/delete_subscription/<subscription_id>", methods=["DELETE"])
def delete_subscription_route(subscription_id):
    
    subscription = get_subscription_by_id(subscription_id)
    deleted_subscription = delete_subscription(subscription)
    
    return jsonify(deleted_subscription.serialize())


#CRUD ROUTES for subscription_type

@subscription_routes.route("/create_subscription_type", methods=["POST"])
def create_subscription_type_route():
    
    data = request.get_json()
    
    new_subscription_type, error = create_subscription_type(data)
    
    if error:
        return jsonify ({"error":error}), 400
    
    return jsonify({
        "message" : "subscriptions type created!",
        "subscription_type_id": new_subscription_type.id,
        "type": new_subscription_type.type,
        "price": new_subscription_type.price
        
    })


@subscription_routes.route("/get_subscription_types", methods=["GET"])
def get_all_subscription_types_route():
    
    subscription_types = get_all_subscription_types()
    
    return jsonify([subscription_type.serialize() for subscription_type in subscription_types])



@subscription_routes.route("/get_subscription_type/<subscription_type_id>", methods=["GET"])
def get_subscription_type_by_id_route(subscription_type_id):
    
    subscription_type = get_subscription_type_by_id(subscription_type_id)
    
    return jsonify(subscription_type)



@subscription_routes.route("/update_subscription_type/<subscription_type_id>", methods=["PUT"])
def update_subscription_type_route(subscription_type_id):
    
    data = request.get_json()
    
    subscription_type = get_subscription_type_by_id(subscription_type_id)
    updated_subscription_type = update_subscription_type(subscription_type, data)
    return jsonify(updated_subscription_type.serialize())



@subscription_routes.route("/delete_subscription_type/<subscription_type_id>", methods=["DELETE"])
def delete_subscription_type_route(subscription_type_id):
    
    subscription_type = get_subscription_type_by_id(subscription_type_id)
    
    deleted_subscription_type = delete_subscription_type(subscription_type)
    return jsonify(deleted_subscription_type.serialize())