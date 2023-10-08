import hashlib
import requests
import os
from dotenv import load_dotenv
from datetime import timedelta

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import jwt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
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
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
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

                        # TODO: [Get the user data from database]
        # --- Just for testing, we will pass user data directly
        user.phone_number = phone_number

        # Check if the phone number is already registered
        if phone_number in user.phone_number:
            return jsonify({'message': 'Phone number is already registered'}), 409

        # # Hash the password securely (you should use a proper password hashing library)
        # hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # --- Just for testing, we will pass user data directly
        user.password_hash = hashed_password

        # Store the user data in the local "database"
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.password_hash = hashed_password

        # TODO: Store the user data in the database

        return jsonify({'message': 'User registered successfully'}), 201


# Endpoint for user login
# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    phone_number = data['phone_number']
    password = data['password']

    # TODO: [Get the user data from database]
    # --- Just for testing, we will pass user data directly
    user.phone_number = phone_number

    # Check if the phone number is registered
    if phone_number not in user.phone_number:
        return jsonify({'message': 'Phone number is not registered'}), 404

    # Hash the password securely (you should use a proper password hashing library)
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # --- Just for testing, we will pass user data directly
    user.password_hash = hashed_password

    # Check if the provided password is correct
    if hashed_password != user.password_hash:
        return jsonify({'message': 'Incorrect password'}), 401

    access_token = create_access_token(identity=phone_number)
    refresh_token = create_refresh_token(identity=phone_number)
    return jsonify(access_token=access_token, refresh_token=refresh_token)
    # return jsonify({'message': 'Logged in successfully', 'user_id': users[phone_number]['user_id']}), 200

# We are using the `refresh=True` options in jwt_required to only allow
# refresh tokens to access this route.
@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token), 200

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/user_information', methods=['GET, POST'])
@jwt_required()
def user_information():
    if request.method == 'GET':
        current_user = get_jwt_identity()
        return jsonify({'message': 'User information', 'user_id': current_user}), 200
    elif request.method == 'POST':
        # TODO: [Update new data in database]
        pass

@app.route('/subscription_manager', methods=['GET', 'POST'])
@jwt_required()
def subscription_manager():
    if request.method == 'GET':
        current_user = get_jwt_identity()
        return jsonify({'message': 'Subscription manager', 'user_id': current_user}), 200
    elif request.method == 'POST':
        # TODO: [Update new data in database]
        # verify user if student or not
        pass

@app.route('/device_manager', methods=['GET', 'POST'])
@jwt_required()
def device_manager():
    if request.method == 'GET':
        current_user = get_jwt_identity()
        return jsonify({'message': 'Device manager', 'user_id': current_user}), 200
    elif request.method == 'POST':
        pass

@app.route('/payment_information', methods=['GET','POST'])
@jwt_required()
def payment_information():
    if request.method == 'GET':
        current_user = get_jwt_identity()
        return jsonify({'message': 'Payment information', 'user_id': current_user}), 200
    elif request.method == 'POST':
        pass

@app.route('/payment_manager', methods=['GET','POST'])
@jwt_required()
def payment_manager():
    if request.method == 'GET':
        current_user = get_jwt_identity()
        return jsonify({'message': 'Payment manager', 'user_id': current_user}), 200
    elif request.method == 'POST':
        pass

if __name__ == '__main__':
    app.run(debug=True)
