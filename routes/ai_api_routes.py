from flask import Flask, request, jsonify, Blueprint
from controllers.ai_api_service import Aimodelfactory


ai_api_routes = Blueprint("ai_api_routes", __name__)


@ai_api_routes.route("/ai_model", methods=["POST"])
def ai_api_call():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
    if "model_type" not in data or not data["model_type"]:
        return jsonify({"error": "Missing required field: 'model_type'"}), 400
    if "prompt" not in data:
        return jsonify({"error": "Missing required field: 'prompt'"}), 400

    model_type = data.get("model_type")
    model = Aimodelfactory.get_model(model_type)
    prompt = data.get("prompt")
    system = data.get("system")
    response = model.generate_response(system, prompt)
    return jsonify({"response": response})
