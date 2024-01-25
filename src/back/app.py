import hashlib
import requests
import os
from dotenv import load_dotenv
from datetime import timedelta

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from user import *
from Database import Database

# import OTP.OTPGeneration as OTP
# from flask-mail import Mail, Message

app = Flask(__name__)

db = Database()

# Load environment variables
load_dotenv()


# Set up the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

user = User()

if __name__ == '__main__':
    import routes
    routes.init()
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context='adhoc')
