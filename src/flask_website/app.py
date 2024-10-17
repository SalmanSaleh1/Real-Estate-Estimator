from dotenv import load_dotenv
import db_connection
from db_classes import Property

import unittest
import os
import subprocess
from flask import Flask, render_template, request, jsonify
from api import api_blueprint  # Import the API blueprint
from test_insertion import TestInsertion


app = Flask(__name__, static_url_path='/static')

# Register the API blueprint
app.register_blueprint(api_blueprint, url_prefix='/api')

# db connections
app = db_connection.app
db = db_connection.db
bcrypt = db_connection.bcrypt

# Home route
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/estimator', methods=['GET'])
def estimator():
    return render_template('estimator.html')
    
# Route for fetching property details using id_object
@app.route('/property-details/<int:id_object>', methods=['GET'])
def get_property_details(id_object):
    property_details = Property.query.filter_by(id_object=id_object).first()

    if property_details:
        # Return property details in the rendered template
        return render_template('property_details.html', property=property_details)
    else:
        return jsonify({'error': 'Property not found'}), 404


@app.route('/run_tests', methods=['GET'])
def run_tests():
    try:
        # Create a test suite
        suite = unittest.TestLoader().loadTestsFromTestCase(TestInsertion)

        # Create a test runner and capture the results
        result = unittest.TextTestRunner(verbosity=2).run(suite)

        # Check if tests passed or failed
        if result.wasSuccessful():
            return jsonify({"message": "Tests ran successfully", "result": result}), 200
        else:
            return jsonify({"error": "Test execution failed", "result": result}), 500

    except Exception as e:
        return jsonify({"error": f"Test execution failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)