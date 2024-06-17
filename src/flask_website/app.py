from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__, static_url_path='/static')

# MongoDB configurations
HOSTNAME = "app_mongodb"
DATABASE_NAME = "app_db"
COLLECTION_NAME = "app_collection"

client = MongoClient(host=HOSTNAME, port=27017)
db = client[DATABASE_NAME][COLLECTION_NAME]


# Homw route
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)