from flask import Blueprint, jsonify, request
from dotenv import load_dotenv
from flask import Blueprint, jsonify
import db_connection
import numpy as np
from db_classes import Property
from load_model import load_xgb_model  # Import the function that loads the model

xgb_model = load_xgb_model()

api_blueprint = Blueprint('api', __name__)

# Database connections
app = db_connection.app
db = db_connection.db
bcrypt = db_connection.bcrypt

# Define an API route that accepts object_id as a parameter in the function signature
@api_blueprint.route('/test/<int:object_id>', methods=['GET'])  # Or POST depending on your use case
def ml_api(object_id):
    """
    This API endpoint takes object_id as a path parameter and uses it to retrieve
    the necessary data for the machine learning model. It only returns the predicted price.
    """

    # Use object_id to retrieve relevant property information from the database
    property_info = get_info(object_id)

    # Check if the property was found
    if 'error' in property_info:
        return jsonify({"error": property_info['error']}), 404

    # Extract the required fields for the ML model from property_info
    city = property_info['city']
    district = property_info['district']
    Mukatat = property_info['Mukatat']
    Piece_num = property_info['Piece_num']
    space = property_info['space']

    # Convert the input features into the format required by the model
    # Preprocess features as needed (e.g., encoding, scaling)
    features = np.array([[city, district, Mukatat, Piece_num, float(space)]])

    # Predict using the loaded model
    try:
        prediction = xgb_model.predict(features)
        return jsonify({"predicted_price": float(prediction[0])})
    except Exception as e:
        return jsonify({"error": f"Model prediction failed: {e}"}), 500

def get_info(object_id):
    """
    Retrieves property details from the database using the provided object_id.
    """
    try:
        # Fetch the property from the database using object id
        property_details = Property.query.filter_by(id_object=object_id).first()

        if property_details:
            # Return the details, renamed to match ML object names
            return {
                "city": property_details.city_name,              # city_name -> city
                "district": property_details.district_name,      # district_name -> district
                "Mukatat": property_details.subdiv_no,           # subdiv_no -> Mukatat
                "Piece_num": property_details.parcel_no,         # parcel_no -> Piece_num
                "space": str(property_details.shape_area)        # shape_area -> space
            }
        else:
            return {"error": "Property not found"}

    except Exception as e:
        # Catch any unexpected errors
        return {"error": f"Error processing input: {e}"}