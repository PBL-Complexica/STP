from flask import Flask, request, jsonify
import hashlib
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# This is just a simple in-memory database for demonstration purposes.
# In a real application, you would use a proper database.
users = {}
user_id_counter = 1  # Initialize the user ID counter


@app.route('/', methods=["GET", "POST"])
def hello_world():
    return "Welcome to STP!", 200


# Endpoint for user signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    # Check if phone number and password are provided
    if 'phone_number' not in data or 'password' not in data:
        return jsonify({'message': 'Phone number and password are required'}), 400

    phone_number = data['phone_number']
    password = data['password']

    # Check if the phone number is already registered
    if phone_number in users:
        return jsonify({'message': 'Phone number is already registered'}), 409

    global user_id_counter  # Access the global user ID counter
    user_id = user_id_counter  # Assign the current user ID
    user_id_counter += 1  # Increment the user ID counter for the next user

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

    return jsonify({'message': 'User registered successfully', 'user_id': user_id}), 201


# Endpoint for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Check if phone number and password are provided
    if 'phone_number' not in data or 'password' not in data:
        return jsonify({'message': 'Phone number and password are required'}), 400

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
