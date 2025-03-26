from flask import Flask, request, jsonify, Blueprint
from controllers.ai_api_service import Aimodelfactory


ai_api_routes = Blueprint("ai_api_routes", __name__)


@ai_api_routes.route("/ai_model", methods=["POST"])
def ai_api_call():

    data = request.get_json()

    model_type = data.get("model_type")
    model = Aimodelfactory.get_model(model_type)
    # User prompt
    prompt = data.get("prompt")
    # System role
    system = data.get("system")
    response = model.generate_response(system, prompt)
    return jsonify({"response": response})
