from flask import Flask, request
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy(app)


@app.route('/', methods=["GET", "POST"])
def hello_world():
    return "Hello User!", 200
