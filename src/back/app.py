import hashlib
import requests
import os
from dotenv import load_dotenv

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migratex

import jwt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from user import *
# import OTP.OTPGeneration as OTP
# from flask-mail import Mail, Message
# import PyJWT.jwt as jwt

app = Flask(__name__)

# Load environment variables
load_dotenv()

#db = SQLAlchemy(app)
#migrate = Migrate(app, db)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")
jwt = JWTManager(app)

user = User()

@app.route('/', methods=["GET"])
def hello_world():
    return "Welcome to STP!", 200


# Endpoint for user signup
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        data = request.get_json()

        phone_number = data['phone_number']
        password = data['password']

        # TODO: Get the user data from database

        # Check if the phone number is already registered
        if phone_number in user.phone_number:
            return jsonify({'message': 'Phone number is already registered'}), 409

        # # Hash the password securely (you should use a proper password hashing library)
        # hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Store the user data in the local "database"
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.password_hash = hashed_password

        # TODO: Store the user data in the database

        return jsonify({'message': 'User registered successfully'}), 201


# Endpoint for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    phone_number = data['phone_number']
    password = data['password']

    # Check if the phone number is registered
    if phone_number not in user.phone_number:
        return jsonify({'message': 'Phone number is not registered'}), 404

    # Hash the password securely (you should use a proper password hashing library)
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Check if the provided password is correct
    if hashed_password != users[phone_number]['password']:
        return jsonify({'message': 'Incorrect password'}), 401

    return jsonify({'message': 'Logged in successfully', 'user_id': users[phone_number]['user_id']}), 200


if __name__ == '__main__':
    app.run(debug=True)
