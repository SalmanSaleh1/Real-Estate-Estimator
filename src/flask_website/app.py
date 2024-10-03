from flask import Flask, render_template, request, jsonify
from api import api_blueprint  # Import the API blueprint

app = Flask(__name__, static_url_path='/static')

# Register the API blueprint
app.register_blueprint(api_blueprint, url_prefix='/api')


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
    
# Route for serving the property details page with API data
@app.route('/property-details')
def property_details():
    parcel_no = request.args.get('parcel_no')
    block_no = request.args.get('block_no')

    # Fetch details from an API or database based on parcel_no and block_no
    # For demonstration, using mock data
    api_data = {
        'parcel_no': parcel_no,
        'block_no': block_no,
        'api_parcel_no': 'API Parcel 12345',
        'api_block_no': 'API Block 67890'
    }

    return render_template('property_details.html', **api_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)