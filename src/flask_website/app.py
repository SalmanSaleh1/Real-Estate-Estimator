from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, Blueprint
import unittest
import os
import requests  # Import requests for making HTTP calls
import db_connection
from db_classes import Property
from api import api_blueprint  # Import the API blueprint
from test_insertion import TestInsertion

# Load environment variables
load_dotenv()

# Initialize the Flask application
app = Flask(__name__, static_url_path='/static')

# Register the API blueprint with the '/api' prefix
app.register_blueprint(api_blueprint, url_prefix='/api')

# Database connections
app = db_connection.app
db = db_connection.db
bcrypt = db_connection.bcrypt

# Home route
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# About route
@app.route('/about')
def about():
    return render_template('about.html')

# Estimator route
@app.route('/estimator', methods=['GET'])
def estimator():
    return render_template('estimator.html')

# Property details route with predicted price from ML API
@app.route('/property/<int:id_object>', methods=['GET'])
def get_property_details(id_object):
    # Retrieve property details from the database
    property_details = Property.query.filter_by(id_object=id_object).first()

    if property_details:
        # Call the ML API to get the predicted price
        try:
            api_url = f'http://127.0.0.1:5000/api/predict/{id_object}'
            response = requests.get(api_url)
            predicted_price = response.json().get('predicted_price', 'N/A') if response.status_code == 200 else 'N/A'
        except Exception as e:
            print(f"Error calling ML API: {e}")
            predicted_price = 'N/A'

        # Render the property details page with property details and predicted price
        return render_template('property_details.html', property=property_details, predicted_price=predicted_price)
    else:
        return jsonify({'error': 'Property not found'}), 404

# Route to run unit tests for insertion functionality
@app.route('/run_tests', methods=['GET'])
def run_tests():
    try:
        # Create a test suite
        suite = unittest.TestLoader().loadTestsFromTestCase(TestInsertion)

        # Run tests and capture the results
        result = unittest.TextTestRunner(verbosity=2).run(suite)

        # Check if tests passed or failed
        if result.wasSuccessful():
            return jsonify({"message": "Tests ran successfully"}), 200
        else:
            return jsonify({"error": "Test execution failed"}), 500
    except Exception as e:
        return jsonify({"error": f"Test execution failed: {str(e)}"}), 500

# Run the application
if __name__ == '__main__':
    # Ensure the app runs on host '0.0.0.0' for external access and set debug mode
    app.run(host='0.0.0.0', port=5000, debug=True)
