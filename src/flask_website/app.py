from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, Blueprint
import unittest
import os
import requests  # Import requests for making HTTP calls
import db_connection
from db_classes import Property
from api import api_blueprint  # Import the API blueprint
from tests.test_insertion import TestInsertion
from tests.test_backend import BackendTest

# Load environment variables
load_dotenv()

# Initialize the Flask application
app = Flask(__name__, static_url_path='/static')

# Register the API blueprint with the '/api' prefix
app.register_blueprint(api_blueprint, url_prefix='/api')

# Database connections (assuming db_connection contains these values)
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
@app.route('/run_script', methods=['GET'])
def run_tests():
    try:
        # Create a test suite for insertion functionality
        suite = unittest.TestLoader().loadTestsFromTestCase(TestInsertion)

        # Run tests and capture the results
        result = unittest.TextTestRunner(verbosity=2).run(suite)

        # Check if tests passed or failed
        if result.wasSuccessful():
            return jsonify({"message": "Tests insertion script run successfully"}), 200
        else:
            return jsonify({"error": "Test execution failed"}), 500
    except Exception as e:
        return jsonify({"error": f"Test execution failed: {str(e)}"}), 500


# Route to run backend unit tests for SQL, API, and app functionality
@app.route('/run_backend_tests', methods=['GET'])
def run_backend_tests():
    try:
        # Create a test suite for backend functionality
        suite = unittest.TestLoader().loadTestsFromTestCase(BackendTest)

        # Capture the test results
        test_results = []
        
        class TestResultHandler(unittest.TextTestResult):
            def addSuccess(self, test):
                super().addSuccess(test)
                test_results.append({"test": str(test), "status": "success"})

            def addFailure(self, test, err):
                super().addFailure(test, err)
                test_results.append({"test": str(test), "status": "failure", "error": self._exc_info_to_string(err, test)})

            def addError(self, test, err):
                super().addError(test, err)
                test_results.append({"test": str(test), "status": "error", "error": self._exc_info_to_string(err, test)})

        # Run the test suite with a custom result handler
        runner = unittest.TextTestRunner(resultclass=TestResultHandler, verbosity=2)
        result = runner.run(suite)

        # Check if tests passed or failed
        if result.wasSuccessful():
            return jsonify({"message": "All tests passed successfully", "results": test_results}), 200
        else:
            return jsonify({"message": "Some tests failed", "results": test_results}), 500

    except Exception as e:
        return jsonify({"error": f"Test execution failed: {str(e)}"}), 500


# Run the application
if __name__ == '__main__':
    # Ensure the app runs on host '0.0.0.0' for external access and set debug mode
    app.run(host='0.0.0.0', port=5000, debug=True)
