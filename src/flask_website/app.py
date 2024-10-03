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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)