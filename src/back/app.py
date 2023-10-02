from flask import Flask, request, jsonify
import hashlib
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migratex
import jwt
from user import *
# import OTP.OTPGeneration as OTP
# from flask-mail import Mail, Message
# import PyJWT.jwt as jwt

app = Flask(__name__)

#db = SQLAlchemy(app)
#migrate = Migrate(app, db)

user = User()
user_phone = UserPhone()
user_email = UserEmail()
user_device = UserDevice()


@app.route('/', methods=["GET", "POST"])
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
        if phone_number in user_phone.phone_number:
            return jsonify({'message': 'Phone number is already registered'}), 409


        # salted_password = user_id + password
        # # Hash the password securely (you should use a proper password hashing library)
        # hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Store the user data in the database
        users[phone_number] = {
            'user_id': user_id,
            'password': hashed_password,
            'phone_number': phone_number
        }

    elif request.method == 'GET':
        data = request.args
        phone_number = data['phone_number']
        password = data['password']

        # Check if the phone number is already registered
        if phone_number in users:
            return jsonify({'message': 'Phone number is already registered'}), 409

        global user_id_counter


    return jsonify({'message': 'User registered successfully', 'user_id': user_id}), 201


# Endpoint for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    phone_number = data['phone_number']
    password = data['password']

    # Check if the phone number is registered
    if phone_number not in users:
        return jsonify({'message': 'Phone number is not registered'}), 404

    # Hash the password securely (you should use a proper password hashing library)
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Check if the provided password is correct
    if hashed_password != users[phone_number]['password']:
        return jsonify({'message': 'Incorrect password'}), 401

    return jsonify({'message': 'Logged in successfully', 'user_id': users[phone_number]['user_id']}), 200


if __name__ == '__main__':
    app.run(debug=True)
