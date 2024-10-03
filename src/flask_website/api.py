from flask import Blueprint, jsonify

# Create a blueprint for the API
api_blueprint = Blueprint('api', __name__)

# Define a simple route for the API
@api_blueprint.route('/test', methods=['GET'])
def test_api():
    return jsonify({"message": "This is a test API route!"})
