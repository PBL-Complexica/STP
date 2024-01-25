import sqlalchemy.dialects.postgresql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import dotenv_values

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = dotenv_values(".env")["DB_URI"]

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class AppUser(db.Model):
    __tablename__ = 'app_user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    birth_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)


class EmailAddress(db.Model):
    __tablename__ = 'email_address'
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False)


class UserEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    email_id = db.Column(db.Integer, db.ForeignKey('email_address.id'), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False)
    removed_at = db.Column(db.DateTime, nullable=True, default='2100-01-01 00:00:00')


class PhoneNumber(db.Model):
    __tablename__ = 'phone_number'
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False)


class UserPhone(db.Model):
    __tablename__ = 'user_phone'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    phone_id = db.Column(db.Integer, db.ForeignKey('phone_number.id'), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False)
    removed_at = db.Column(db.DateTime, nullable=True, default='2100-01-01 00:00:00')


class Device(db.Model):
    __tablename__ = 'device'
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(50), nullable=False, unique=True)
    # device_sn = db.Column(db.String(), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False)


class UserDevice(db.Model):
    __tablename__ = 'user_device'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    removed_at = db.Column(db.DateTime, nullable=True, default='2100-01-01 00:00:00')


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False)


class UserCategory(db.Model):
    __tablename__ = 'user_category'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    removed_at = db.Column(db.DateTime, nullable=True, default='2100-01-01 00:00:00')


class SubscriptionType(db.Model):
    __tablename__ = 'subscription_type'
    id = db.Column(db.Integer, primary_key=True)
    subscription_type_name = db.Column(db.String(50), nullable=False, unique=True)
    months = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


class Subscription(db.Model):
    __tablename__ = 'subscription'
    id = db.Column(db.Integer, primary_key=True)
    subscription_type_id = db.Column(db.Integer, db.ForeignKey('subscription_type.id'), nullable=False)
    valid_from = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


class UserSubscription(db.Model):
    __tablename__ = 'user_subscription'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    removed_at = db.Column(db.DateTime, nullable=True, default='2100-01-01 00:00:00')
