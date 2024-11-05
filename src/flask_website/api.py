from flask import Flask, Blueprint, jsonify, request, render_template_string
from load_model import load_catboost_model
import numpy as np
import pandas as pd
from catboost import Pool
import db_connection
from db_classes import Property

# Initialize Blueprint
api_blueprint = Blueprint('api', __name__)

# Database connections
app = db_connection.app
db = db_connection.db
bcrypt = db_connection.bcrypt

# Load the CatBoost model
catboost_model = load_catboost_model()

# Prediction function
def predict_property_value(area, city, district, Mukatat, space, property_classification, property_type, Price_per_square_meter=None):
    # Prepare data dictionary for prediction
    data = {
        'area': [area],
        'city': [city],
        'district': [district],
        'Mukatat': [Mukatat],
        'property_classification': [property_classification],
        'property_type': [property_type],
        'space': [space],
        'log_space': [np.log1p(space)]
    }

    if Price_per_square_meter is not None:
        data['Price_per_square_meter'] = [Price_per_square_meter]

    new_data = pd.DataFrame(data)
    new_data = new_data.reindex(columns=catboost_model.feature_names_, fill_value="unknown")
    
    categorical_features = ['area', 'city', 'district', 'Mukatat', 'property_classification', 'property_type', 'Price_per_square_meter']
    for col in categorical_features:
        if col in new_data.columns:
            new_data[col] = new_data[col].astype(str)
    
    input_pool = Pool(new_data, cat_features=categorical_features)
    log_price_pred = catboost_model.predict(input_pool)
    predicted_price = np.expm1(log_price_pred)
    
    return predicted_price[0]

# Prediction API endpoint
@api_blueprint.route('/predict/<int:object_id>', methods=['GET'])
def ml_api(object_id):
    property_info = get_info(object_id)
    if 'error' in property_info:
        return jsonify({"error": property_info['error']}), 404

    try:
        prediction = predict_property_value(
            area=property_info['area'],
            city=property_info['city'],
            district=property_info['district'],
            Mukatat=property_info['Mukatat'],
            space=float(property_info['space']),
            property_classification=property_info.get('property_classification', 'unknown'),
            property_type=property_info.get('property_type', 'unknown'),
            Price_per_square_meter=property_info.get('Price_per_square_meter', None)
        )
        return jsonify({"predicted_price": prediction})

    except Exception as e:
        return jsonify({"error": f"Model prediction failed: {e}"}), 500

# Database retrieval function
def get_info(object_id):
    try:
        property_details = Property.query.filter_by(id_object=object_id).first()
        if property_details:
            return {
                "area": "منطقة القصيم",
                "city": "بريده",
                "district": property_details.district_name,
                "Mukatat": property_details.subdiv_no,
                "space": property_details.shape_area,
                "property_classification": property_details.parcel_land_use,
                "property_type": "أرض", 
                "Price_per_square_meter": getattr(property_details, 'Price_per_square_meter', None)
            }
        else:
            return {"error": "Property not found"}
    except Exception as e:
        return {"error": f"Error processing input: {e}"}

# Test endpoints
@api_blueprint.route('/test_prediction', methods=['GET'])
def test_prediction():
    try:
        predicted_price = predict_property_value(
            area="منطقة الرياض",
            city="الرياض",
            district="الزهرة",
            Mukatat="1017",
            property_classification="سكني",
            property_type="قطعة أرض",
            space=400.0
        )
        return jsonify({"predicted_price": predicted_price})
    except Exception as e:
        return jsonify({"error": f"Test prediction failed: {e}"}), 500

@api_blueprint.route('/test', methods=['GET'])
def test():
    try:
        return render_template_string("<html><body><h1>Hello, World!</h1></body></html>")
    except Exception as e:
        return jsonify({"error": f"Test prediction failed: {e}"}), 500

# Register the blueprint with a URL prefix
app.register_blueprint(api_blueprint, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)
