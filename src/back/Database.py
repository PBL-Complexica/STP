from flask_migrate import upgrade
import psycopg2
from datetime import datetime
from db_model import app
from dotenv import dotenv_values
from bcrypt import gensalt, hashpw, checkpw
import re


class DatabaseMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(DatabaseMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=DatabaseMeta):
    def __init__(self):
        with app.app_context():
            upgrade()

        # Load environment variables
        config = dotenv_values(".env")
        self.db = psycopg2.connect(
            host=config["DB_HOST"],
            database=config["DB_DATABASE"],
            user=config["DB_USER"],
            password=config["DB_PASSWORD"]
        )
        self.cursor = self.db.cursor()

        # TODO: Remove unconfirmed users
        # self.remove_unconfirmed()

        # Populate database with initial data
        self.__populate()

    # Private methods
    # Insert new user
    def __insert_user(self, first_name, last_name, password_hash, birth_date=None):
        self.cursor.execute(
            "INSERT INTO app_user (first_name, last_name, password_hash, birth_date, created_at, confirmed, active) "
            "VALUES (%s, %s, %s, %s, %s, FALSE, TRUE)",
            (first_name, last_name, password_hash, birth_date, datetime.now())
        )
        self.db.commit()

    def __get_user_id(self, first_name, last_name, password_hash):
        self.cursor.execute(
            "SELECT id FROM app_user WHERE first_name = %s AND last_name = %s AND password_hash = %s",
            (first_name, last_name, password_hash)
        )
        return self.cursor.fetchone()

    # Insert new email
    def __insert_email(self, email_address):
        self.cursor.execute(
            "INSERT INTO email_address (email_address, created_at) "
            "VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (email_address, datetime.now())
        )
        self.db.commit()

    # Get email address id
    def __get_email_id(self, email_address):
        self.cursor.execute(
            "SELECT id FROM email_address WHERE email_address = %s",
            (email_address,)
        )
        return self.cursor.fetchone()

    # Get phone number id
    def __get_phone_id(self, phone_number):
        self.cursor.execute(
            "SELECT id FROM phone_number WHERE phone_number = %s",
            (phone_number,)
        )
        return self.cursor.fetchone()

    # Get device id
    def __get_device_id(self, serial_number):
        self.cursor.execute(
            "SELECT id FROM device WHERE device_sn = %s",
            (serial_number,)
        )
        return self.cursor.fetchone()

    # Insert new phone number
    def __insert_phone(self, phone_number):
        self.cursor.execute(
            "INSERT INTO phone_number (phone_number, created_at) "
            "VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (phone_number, datetime.now())
        )
        self.db.commit()

    # Insert new device
    def __insert_device(self, serial_number, device_name):
        self.cursor.execute(
            "INSERT INTO device (device_name, device_sn, created_at) "
            "VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
            (device_name, serial_number, datetime.now())
        )
        self.db.commit()

    # Return user's for a given active email address
    def __get_user_id_email(self, email_address):
        self.cursor.execute(
            "SELECT user_id FROM user_email "
            "WHERE email_id = %s AND removed_at > %s",
            (self.__get_email_id(email_address), datetime.now())
        )
        return self.cursor.fetchall()

    # Return user's for a given active phone number
    def __get_user_id_phone(self, phone_number):
        self.cursor.execute(
            "SELECT user_id FROM user_phone "
            "WHERE phone_id = %s AND removed_at > %s",
            (self.__get_phone_id(phone_number), datetime.now())
        )
        return self.cursor.fetchall()

    # Return devices associated with a user device
    def __get_user_id_device(self, serial_number):
        self.cursor.execute(
            "SELECT user_id FROM user_device "
            "WHERE device_id = %s AND removed_at > %s",
            (self.__get_device_id(serial_number), datetime.now())
        )
        return self.cursor.fetchall()

    # Connect user to email address
    def __insert_user_email(self, user_id, email_id):
        self.cursor.execute(
            "INSERT INTO user_email (user_id, email_id, created_at, confirmed, removed_at) "
            "VALUES (%s, %s, %s, FALSE, '2100-01-01') ON CONFLICT DO NOTHING",
            (user_id, email_id, datetime.now())
        )
        self.db.commit()

    # Connect user to phone number
    def __insert_user_phone(self, user_id, phone_id):
        self.cursor.execute(
            "INSERT INTO user_phone (user_id, phone_id, created_at, confirmed, removed_at) "
            "VALUES (%s, %s, %s, FALSE, '2100-01-01') ON CONFLICT DO NOTHING",
            (user_id, phone_id, datetime.now())
        )
        self.db.commit()

    # Connect user to device
    def __insert_user_device(self, user_id, device_id):
        self.cursor.execute(
            "INSERT INTO user_device (user_id, device_id, created_at, removed_at) "
            "VALUES (%s, %s, %s, '2100-01-01') ON CONFLICT DO NOTHING",
            (user_id, device_id, datetime.now())
        )
        self.db.commit()

    # Add subscription types with months and prices
    def __add_categories(self, name: str, prices: list):
        self.cursor.execute(
            "INSERT INTO subscription_type (subscription_type_name, months, cost, created_at) "
            "VALUES (%s, %s, %s, %s) "
            "ON CONFLICT DO NOTHING",
            (name + "-1", 1, prices[0], datetime.now())
        )
        self.cursor.execute(
            "INSERT INTO subscription_type (subscription_type_name, months, cost, created_at) "
            "VALUES (%s, %s, %s, %s) "
            "ON CONFLICT DO NOTHING",
            (name + "-3", 3, prices[1], datetime.now())
        )
        self.cursor.execute(
            "INSERT INTO subscription_type (subscription_type_name, months, cost, created_at) "
            "VALUES (%s, %s, %s, %s) O"
            "N CONFLICT DO NOTHING",
            (name + "-6", 6, prices[2], datetime.now())
        )
        self.db.commit()

    def __add_user_categories(self, name: str):
        self.cursor.execute(
            "INSERT INTO category (category_name, created_at) "
            "VALUES (%s, %s) "
            "ON CONFLICT DO NOTHING",
            (name, datetime.now())
        )
        self.db.commit()

    # Populate database with initial data
    def __populate(self):
        self.__add_categories("G", [234, 594, 972])
        self.__add_categories("ST", [164, 416, 680])
        self.__add_categories("E", [117, 297, 486])
        self.__add_categories("AE", [234, 594, 972])
        self.__add_categories("FM", [140, 356, 583])
        self.__add_categories("FC", [117, 297, 483])
        self.__add_categories("DI", [164, 416, 680])
        self.__add_categories("DM", [164, 416, 680])
        self.__add_user_categories("general")
        self.__add_user_categories("student")
        self.__add_user_categories("elev")
        self.__add_user_categories("agent economic")
        self.__add_user_categories("familie monoparentala")
        self.__add_user_categories("familie cu multi copii")
        self.__add_user_categories("personal didactic")
        self.__add_user_categories("personal medical")

    # Public methods
    # Remove unconfirmed users
    def remove_unconfirmed(self):
        self.cursor.execute(
            "DELETE FROM app_user WHERE confirmed = FALSE"
        )
        self.db.commit()

    # Confirm user's email address
    def confirm_email(self, email_address):
        self.cursor.execute(
            "UPDATE user_email SET confirmed = TRUE "
            "WHERE email_id = (SELECT id FROM email_address WHERE email_address = %s) AND removed_at > %s",
            (email_address, datetime.now())
        )
        self.db.commit()

    # Confirm user's phone number
    def confirm_phone(self, phone_number):
        self.cursor.execute(
            "UPDATE user_phone SET confirmed = TRUE "
            "WHERE phone_id = (SELECT id FROM phone_number WHERE phone_number = %s) AND removed_at > %s",
            (phone_number, datetime.now())
        )
        self.db.commit()

    # Create new user and associate it with an email, phone number and device
    def register(
            self,
            first_name: str,
            last_name: str,
            password: str,
            email_address: str,
            device_name: str = None,
            device_sn: str = None,
            phone_number: str = None,
            birth_date: str = None
    ) -> dict:
        response = {"type": "", "data": {}}

        # Check email address is valid format
        email_address_ids = self.__get_user_id_email(email_address)
        if not re.match(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", email_address):
            response["type"] = "error"
            response["data"]["email_error"] = 2
            response["data"]["email_message"] = "Invalid email address"
        else:
            self.__insert_email(email_address)

            if email_address_ids:
                response["type"] = "error"
                response["data"]["email_error"] = 1
                response["data"]["email_message"] = "Email already in use"
            else:
                response["data"]["email_error"] = 0
                response["data"]["email_message"] = "Email available"

        # Check phone number is valid format
        phone_number_ids = self.__get_user_id_phone(phone_number)
        if not ((len(phone_number) == 8 and (phone_number[0] == "6" or phone_number[0] == "7")) or (
                len(phone_number) == 9 and (phone_number[0:2] == "06" or phone_number[0:2] == "07")) or (
                        len(phone_number) == 12 and (phone_number[0:5] == "+3736" or phone_number[0:5] == "+3737"))):
            response["type"] = "error"
            response["data"]["phone_error"] = 2
            response["data"]["phone_message"] = "Invalid phone number"
        else:
            self.__insert_phone(phone_number)

            if phone_number_ids:
                response["type"] = "error"
                response["data"]["phone_error"] = 1
                response["data"]["phone_message"] = "Phone number already in use"
            else:
                response["data"]["phone_error"] = 0
                response["data"]["phone_message"] = "Phone number available"

        # Insert device name and serial number
        device_ids = self.__get_user_id_device(device_sn)
        if len(device_sn) != 11:
            response["type"] = "error"
            response["data"]["device_error"] = 2
            response["data"]["device_message"] = "Invalid device serial number"
        else:
            self.__insert_device(device_sn, device_name)

            if device_ids:
                response["type"] = "error"
                response["data"]["device_error"] = 1
                response["data"]["device_message"] = "Device already in use"
            else:
                response["data"]["device_error"] = 0
                response["data"]["device_message"] = "Device available"

        # Check first name is valid format
        if first_name == "" or not first_name.isalpha:
            response["type"] = "error"
            response["data"]["first_name_error"] = 2
            response["data"]["first_name_message"] = "Invalid first name"

        # Check last name is valid format
        if last_name == "" or not last_name.isalpha:
            response["type"] = "error"
            response["data"]["last_name_error"] = 2
            response["data"]["last_name_message"] = "Invalid last name"

        # Check password is valid format
        if len(password) < 8:
            response["type"] = "error"
            response["data"]["password_error"] = 2
            response["data"]["password_message"] = "Invalid password, must be at least 8 characters long"
        else:
            hashed = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

            if response["type"] != "error":
                self.__insert_user(first_name, last_name, hashed, birth_date)
                user_id = self.__get_user_id(first_name, last_name, hashed)[0]
                email_address_id = self.__get_email_id(email_address)[0]
                phone_number_id = self.__get_phone_id(phone_number)[0]
                device_id = self.__get_device_id(device_sn)[0]
                self.__insert_user_email(user_id, email_address_id)
                self.__insert_user_phone(user_id, phone_number_id)
                self.__insert_user_device(user_id, device_id)

                response["type"] = "success"
                response["data"]["message"] = "User registered successfully"
                response["data"]["user_id"] = user_id
                response["data"]["first_name"] = first_name
                response["data"]["last_name"] = last_name
                response["data"]["email_address"] = email_address
                response["data"]["email_id"] = email_address_id
                response["data"]["phone_number"] = phone_number
                response["data"]["phone_id"] = phone_number_id
                response["data"]["device_name"] = device_name
                response["data"]["device_sn"] = device_sn
                response["data"]["device_id"] = device_id
                response["data"]["birth_date"] = birth_date

        return response

    # Login user
    # TODO: Add phone login option
    def login(self, credential: str, password: str) -> dict:
        response = {"type": "", "data": {}}
        password_hash = None
        email_auth = False
        phone_auth = False

        # Check if credential is email
        if re.match(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", credential):
            email_auth = True
        # Check if credential is phone number
        elif ((len(credential) == 8 and (credential[0] == "6" or credential[0] == "7")) or (
               len(credential) == 9 and (credential[0:2] == "06" or credential[0:2] == "07")) or (
               len(credential) == 12 and (credential[0:5] == "+3736" or credential[0:5] == "+3737"))) and (
               credential[-7:].isdigit()):
            phone_auth = True
        # Send error if credential is not email or phone number
        else:
            response["type"] = "error"
            response["data"]["email_error"] = 2
            response["data"]["email_message"] = "Invalid email address"
            response["data"]["phone_error"] = 2
            response["data"]["phone_message"] = "Invalid phone number"

        # If credential is email, check if email is registered
        if email_auth:
            email_address_id = self.__get_email_id(credential)

            # If email is not registered, send error
            if not email_address_id:
                response["type"] = "error"
                response["data"]["email_error"] = 1
                response["data"]["email_message"] = "Email not registered"
                return response
            # If email is registered, get password hash
            else:
                email_address_id = email_address_id[0]

                self.cursor.execute(
                    "SELECT password_hash FROM app_user "
                    "WHERE id = (SELECT user_id FROM user_email WHERE email_id = %s)",
                    (email_address_id,)
                )
                password_hash = self.cursor.fetchone()
        # If credential is phone number, check if phone number is registered
        elif phone_auth:
            phone_number_id = self.__get_phone_id(credential)
            # If phone number is not registered, send error
            if not phone_number_id:
                response["type"] = "error"
                response["data"]["phone_error"] = 1
                response["data"]["phone_message"] = "Phone number not registered"

                return response
            # If phone number is registered, get password hash
            else:
                phone_number_id = phone_number_id[0]

                self.cursor.execute(
                    "SELECT password_hash FROM app_user "
                    "WHERE id = (SELECT user_id FROM user_phone WHERE phone_id = %s)",
                    (phone_number_id,)
                )
                password_hash = self.cursor.fetchone()

        # If password hash is empty, send error for non-existent user
        if not password_hash:
            response["type"] = "error"
            # If credential is email, send email error
            if email_auth:
                response["data"]["email_error"] = 1
                response["data"]["email_message"] = "Email not registered"
            # If credential is phone number, send phone number error
            elif phone_auth:
                response["data"]["phone_error"] = 1
                response["data"]["phone_message"] = "Phone number not registered"

            return response

        # If password is incorrect, send error
        if not checkpw(password.encode('utf-8'), password_hash[0].encode('utf-8')):
            response["type"] = "error"
            response["data"]["password_error"] = 2
            response["data"]["password_message"] = "Incorrect password"
            return response
        # If password is correct, get user data
        else:
            # Get user data based on email
            if email_auth:
                # Get user data
                self.cursor.execute(
                    "SELECT * FROM app_user "
                    "WHERE id = %s",
                    (email_address_id,)
                )
                user = self.cursor.fetchone()
            # Get user data based on phone number
            elif phone_auth:
                self.cursor.execute(
                    "SELECT * FROM app_user "
                    "WHERE id = %s",
                    (phone_number_id,)
                )
                user = self.cursor.fetchone()

            # Get user's email address based on user's id
            self.cursor.execute(
                "SELECT email_address, id FROM email_address "
                "WHERE id = (SELECT email_id FROM user_email WHERE user_id = %s)",
                (user[0],)
            )
            email_address, email_address_id = self.cursor.fetchone()[0]

            # Get user's phone number based on user's id
            self.cursor.execute(
                "SELECT phone_number, id FROM phone_number "
                "WHERE id = (SELECT phone_id FROM user_phone WHERE user_id = %s)",
                (user[0],)
            )
            phone_number, phone_number_id = self.cursor.fetchone()

            # Get user's device data based on user's id
            self.cursor.execute(
                "SELECT device_name, device_sn, id FROM device "
                "WHERE id = (SELECT device_id FROM user_device WHERE user_id = %s)",
                (user[0],)
            )
            device_name, device_sn, device_id = self.cursor.fetchone()

            response["type"] = "success"
            response["data"]["message"] = "User logged in successfully"
            response["data"]["user_id"] = user[0]
            response["data"]["first_name"] = user[1]
            response["data"]["last_name"] = user[2]
            response["data"]["email_address"] = email_address
            response["data"]["email_id"] = email_address_id
            response["data"]["phone_number"] = phone_number
            response["data"]["phone_id"] = phone_number_id
            response["data"]["device_name"] = device_name
            response["data"]["device_sn"] = device_sn
            response["data"]["device_id"] = device_id
            response["data"]["birth_date"] = user[4].strftime("%Y-%m-%d")

            return response

