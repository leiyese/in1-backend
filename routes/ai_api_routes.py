from flask import Flask, request, jsonfiy, Blueprint
from controllers.ai_api_service import Aimodelfactory


ai_api_routes = Blueprint("ai_api_routes", __name__)

@ai_api_routes.route('/ai_model', method = ['POST'])
def ai_api_route():

    model_type = request.get_json()
    model = Aimodelfactory.get_model(model_type)
    #User prompt
    prompt = request.get_json()
    #System role
    system = request.get_json() 
    response = model.generate_response(system, prompt)
    return jsonfiy({"response": response})
