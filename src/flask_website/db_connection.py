import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# SQLAlchemy configuration
HOSTNAME = os.getenv('HOSTNAME')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
DB_PORT = os.getenv('DB_PORT')
MYSQL_ROOT_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
SCHEMA = os.getenv("SCHEMA")

# Check if all required environment variables are set
if not all([HOSTNAME, MYSQL_DATABASE, DB_PORT, MYSQL_ROOT_PASSWORD, MYSQL_USER, MYSQL_PASSWORD, SCHEMA]):
    raise ValueError("One or more environment variables are missing. Please check your .env file.")

# Create the SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{HOSTNAME}:{DB_PORT}/{SCHEMA}?charset=utf8mb4'
app.config['SQLALCHEMY_POOL_SIZE'] = 500
app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600

# Initialize SQLAlchemy and Bcrypt
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)