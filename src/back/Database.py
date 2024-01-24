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
    @staticmethod
    def __handle_response(
            email_error=0,
            phone_error=0,
            password_error=0,
            device_error=0,
            payload: dict = None
    ) -> dict:
        response = {"type": "success", "data": {}}
        response["data"]["email_error"] = email_error
        response["data"]["phone_error"] = phone_error
        response["data"]["password_error"] = password_error
        response["data"]["device_error"] = device_error

        if any([email_error, phone_error, password_error, device_error]) != 0:
            response["type"] = "error"

        if email_error == 0:
            response["data"]["email_message"] = "Email success"
        elif email_error == 1:
            response["data"]["email_message"] = "Email in use"
        elif email_error == 2:
            response["data"]["email_message"] = "Invalid email address"

        if phone_error == 0:
            response["data"]["phone_message"] = "Phone success"
        elif phone_error == 1:
            response["data"]["phone_message"] = "Phone in use"
        elif phone_error == 2:
            response["data"]["phone_message"] = "Invalid phone number"

        if password_error == 0:
            response["data"]["password_message"] = "Password success"
        elif password_error == 1:
            response["data"]["password_message"] = "Password incorrect"
        elif password_error == 2:
            response["data"]["password_message"] = "Invalid password"

        if device_error == 0:
            response["data"]["device_message"] = "Device success"
        elif device_error == 1:
            response["data"]["device_message"] = "Device in use"
        elif device_error == 2:
            response["data"]["device_message"] = "Invalid device name"

        if payload is not None:
            for key in payload.keys():
                response["data"][key] = payload[key]

        return response

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
        if (len(phone_number) == 8 or len(phone_number) == 9) and phone_number.isdigit():
            phone_number = "+373" + phone_number[-8:]

        self.cursor.execute(
            "SELECT id FROM phone_number WHERE phone_number = %s",
            (phone_number,)
        )
        return self.cursor.fetchone()

    # Get device id
    def __get_device_id(self, device_name):
        self.cursor.execute(
            "SELECT id FROM device WHERE device_name = %s",
            (device_name,)
        )
        return self.cursor.fetchone()

    # Insert new phone number
    def __insert_phone(self, phone_number):
        if (len(phone_number) == 8 or len(phone_number) == 9) and phone_number.isdigit():
            phone_number = "+373" + phone_number[-8:]

        self.cursor.execute(
            "INSERT INTO phone_number (phone_number, created_at) "
            "VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (phone_number, datetime.now())
        )
        self.db.commit()

    # Insert new device
    def __insert_device(self, device_name):
        self.cursor.execute(
            "INSERT INTO device (device_name, created_at) "
            "VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (device_name, datetime.now())
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

    def __update_first_name(self, user_id, first_name):
        self.cursor.execute(
            "UPDATE app_user SET first_name = %s "
            "WHERE id = %s",
            (first_name, user_id)
        )
        # self.db.commit()

    def __update_last_name(self, user_id, last_name):
        self.cursor.execute(
            "UPDATE app_user SET last_name = %s "
            "WHERE id = %s",
            (last_name, user_id)
        )

    def __update_email(self, user_id, email_address):
        self.cursor.execute(
            "UPDATE user_email SET email_id = (SELECT id FROM email_address WHERE email_address = %s) "
            "WHERE user_id = %s",
            (email_address, user_id)
        )

    def __update_phone(self, user_id, phone_number):
        self.cursor.execute(
            "UPDATE user_phone SET phone_id = (SELECT id FROM phone_number WHERE phone_number = %s) "
            "WHERE user_id = %s",
            (phone_number, user_id)
        )

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
            "VALUES (%s, %s, %s, %s)"
            "ON CONFLICT DO NOTHING",
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
    def confirm_email(self, email_address) -> dict:
        response = {"type": "", "data": {}}

        email_address_id = self.__get_email_id(email_address)
        if len(email_address_id) == 0:
            response["type"] = "error"
            response["data"]["email_error"] = 1
            response["data"]["email_message"] = "Email address not registered"
            return response

        self.cursor.execute(
            "UPDATE user_email SET confirmed = TRUE "
            "WHERE email_id = (SELECT id FROM email_address WHERE email_address = %s) AND removed_at > %s",
            (email_address, datetime.now())
        )
        self.db.commit()

        response["type"] = "success"
        response["data"]["email_error"] = 0
        response["data"]["email_message"] = "Email address confirmed successfully"

        return response

    # Confirm user's phone number
    def confirm_phone(self, phone_number) -> dict:
        response = {"type": "", "data": {}}

        if (len(phone_number) == 8 or len(phone_number) == 9) and phone_number.isdigit():
            phone_number = "+373" + phone_number[-8:]

        phone_id = self.__get_phone_id(phone_number)
        if len(phone_id) == 0:
            response["type"] = "error"
            response["data"]["phone_error"] = 1
            response["data"]["phone_message"] = "Phone number not registered"
            return response

        self.cursor.execute(
            "UPDATE user_phone SET confirmed = TRUE "
            "WHERE phone_id = (SELECT id FROM phone_number WHERE phone_number = %s) AND removed_at > %s",
            (phone_number, datetime.now())
        )
        self.db.commit()

        response["type"] = "success"
        response["data"]["phone_error"] = 0
        response["data"]["phone_message"] = "Phone number confirmed successfully"

        return response

    # Confirm user profile
    def confirm_user(self, credential) -> dict:
        response = {"type": "", "data": {}}
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
            return response

        if email_auth:
            self.cursor.execute(
                "UPDATE app_user SET confirmed = TRUE "
                "WHERE id = (SELECT user_id FROM user_email WHERE email_id = (SELECT id FROM email_address WHERE email_address = %s))",
                (credential,)
            )

        elif phone_auth:
            self.cursor.execute(
                "UPDATE app_user SET confirmed = TRUE "
                "WHERE id = (SELECT user_id FROM user_phone WHERE phone_id = (SELECT id FROM phone_number WHERE phone_number = %s))",
                (credential,)
            )

        response["type"] = "success"
        response["data"]["message"] = "User confirmed successfully"

        return response

    # Create new user and associate it with an email, phone number and device
    def register(
            self,
            first_name: str,
            last_name: str,
            password: str,
            email_address: str,
            phone_number: str,
            device_name: str = None,
            birth_date: str = None
    ) -> dict:
        email_error = 0
        phone_error = 0
        password_error = 0
        device_error = 0
        payload = {}

        # Check email address is valid format
        email_address_ids = self.__get_user_id_email(email_address)
        if not re.match(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", email_address):
            email_error = 2
        else:
            self.__insert_email(email_address)

            if email_address_ids:
                email_error = 1
            else:
                email_error = 0

        # Check phone number is valid format
        phone_number_ids = self.__get_user_id_phone(phone_number)
        if not ((len(phone_number) == 8 and (phone_number[0] == "6" or phone_number[0] == "7")) or (
                len(phone_number) == 9 and (phone_number[0:2] == "06" or phone_number[0:2] == "07")) or (
                        len(phone_number) == 12 and (phone_number[0:5] == "+3736" or phone_number[0:5] == "+3737"))):
            phone_error = 2
        else:
            self.__insert_phone(phone_number)

            if phone_number_ids:
                phone_error = 1
            else:
                phone_error = 0

        self.__insert_device(device_name)

        # Check first name is valid format
        if first_name == "" or not first_name.isalpha:
            # TODO
            ...

        # Check last name is valid format
        if last_name == "" or not last_name.isalpha:
            # TODO
            ...

        # Check password is valid format
        if len(password) < 8:
            password_error = 2
        else:
            hashed = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

            if password_error == 0:
                self.__insert_user(first_name, last_name, hashed, birth_date)
                user_id = self.__get_user_id(first_name, last_name, hashed)[0]
                email_address_id = self.__get_email_id(email_address)[0]
                phone_number_id = self.__get_phone_id(phone_number)[0]
                self.__insert_user_email(user_id, email_address_id)
                self.__insert_user_phone(user_id, phone_number_id)

                if device_name is not None:
                    device_id = self.__get_device_id(device_name)[0]
                    self.__insert_user_device(user_id, device_id)
                    payload["device_id"] = device_id
                else:
                    payload["device_id"] = None

                payload["message"] = "User registered successfully"
                payload["user_id"] = user_id
                payload["first_name"] = first_name
                payload["last_name"] = last_name
                payload["email_address"] = email_address
                payload["email_id"] = email_address_id
                payload["phone_number"] = phone_number
                payload["phone_id"] = phone_number_id
                payload["device_name"] = device_name
                payload["birth_date"] = birth_date

        return self.__handle_response(email_error, phone_error, password_error, device_error, payload)

    # Login user
    def login(self, credential: str, password: str) -> dict:
        email_error = 0
        phone_error = 0
        password_error = 0
        device_error = 0
        payload = {}
        password_hash = None
        email_auth = False
        phone_auth = False

        phone_number_id = None
        email_address_id = None

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
            email_error = 2
            phone_error = 2

        # If credential is email, check if email is registered
        if email_auth:
            email_address_id = self.__get_email_id(credential)

            # If email is not registered, send error
            if not email_address_id:
                email_error = 1
                return self.__handle_response(email_error, phone_error, password_error, device_error, payload)
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
                phone_error = 1

                return self.__handle_response(email_error, phone_error, password_error, device_error, payload)
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
            # If credential is email, send email error
            if email_auth:
                email_error = 1
            # If credential is phone number, send phone number error
            elif phone_auth:
                phone_error = 1

            return self.__handle_response(email_error, phone_error, password_error, device_error, payload)

        # If password is incorrect, send error
        if not checkpw(password.encode('utf-8'), password_hash[0].encode('utf-8')):
            password_error = 2
            return self.__handle_response(email_error, phone_error, password_error, device_error, payload)
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

                # Get user's email address based on user's id
                return self.get_user_by_id(user[0])
            # Get user data based on phone number
            elif phone_auth:
                self.cursor.execute(
                    "SELECT * FROM app_user "
                    "WHERE id = %s",
                    (phone_number_id,)
                )
                user = self.cursor.fetchone()

                # Get user's email address based on user's id
                return self.get_user_by_id(user[0])

    def get_user_by_id(self, user_id) -> dict:
        email_error = 0
        phone_error = 0
        password_error = 0
        device_error = 0
        payload = {}

        # Get user data based on id
        self.cursor.execute(
            "SELECT * FROM app_user "
            "WHERE id = %s",
            (user_id,)
        )
        user = self.cursor.fetchone()

        if not user:
            email_error = 2
            phone_error = 2
            password_error = 2
            device_error = 2
            payload["message"] = "User not found"
            return self.__handle_response(email_error, phone_error, password_error, device_error, payload)

        # Get user's email address based on user's id
        self.cursor.execute(
            "SELECT email_address, id FROM email_address "
            "WHERE id = (SELECT email_id FROM user_email WHERE user_id = %s)",
            (user[0],)
        )
        email_address, email_address_id = self.cursor.fetchone()

        # Get user's phone number based on user's id
        self.cursor.execute(
            "SELECT phone_number, id FROM phone_number "
            "WHERE id = (SELECT phone_id FROM user_phone WHERE user_id = %s)",
            (user[0],)
        )
        phone_number, phone_number_id = self.cursor.fetchone()

        # Get user's device data based on user's id
        self.cursor.execute(
            "SELECT device_name, id FROM device "
            "WHERE id = (SELECT device_id FROM user_device WHERE user_id = %s)",
            (user[0],)
        )
        device_name, device_id = self.cursor.fetchone()

        payload["user_id"] = user[0]
        payload["message"] = "User logged in successfully"
        payload["first_name"] = user[1]
        payload["last_name"] = user[2]
        payload["email_address"] = email_address
        payload["email_id"] = email_address_id
        payload["phone_number"] = phone_number
        payload["phone_id"] = phone_number_id
        payload["device_name"] = device_name
        payload["device_id"] = device_id
        payload["birth_date"] = user[4].strftime("%Y-%m-%d") if user[4] is not None else None

        return self.__handle_response(email_error, phone_error, password_error, device_error, payload)

    def check_password(self, user_id, password: str) -> dict:
        email_error = 0
        phone_error = 0
        password_error = 0
        device_error = 0
        payload = {}

        # Get current password hash based on id
        self.cursor.execute(
            "SELECT password_hash FROM app_user "
            "WHERE id = %s",
            (user_id,)
        )
        password_hash = self.cursor.fetchone()

        if not password_hash:
            email_error = 2
            phone_error = 2
            password_error = 2
            device_error = 2
            payload["message"] = "User not found"
            return self.__handle_response(email_error, phone_error, password_error, device_error, payload)

        # If password is incorrect, send error
        if not checkpw(password.encode('utf-8'), password_hash[0].encode('utf-8')):
            password_error = 2
            payload["message"] = "Password incorrect"
            return self.__handle_response(email_error, phone_error, password_error, device_error, payload)

        payload["message"] = "Password correct"
        return self.__handle_response(email_error, phone_error, password_error, device_error, payload)

    def change_password(self, user_id, old_password: str, new_password: str) -> dict:
        email_error = 0
        phone_error = 0
        password_error = 0
        device_error = 0
        payload = {}

        response_check = self.check_password(user_id, old_password)
        if response_check["type"] == "error":
            return response_check

        # Check password is valid format
        if len(new_password) < 8:
            password_error = 2
            payload["message"] = "New password is too short"
        else:
            hashed = hashpw(new_password.encode('utf-8'), gensalt()).decode('utf-8')

            if password_error == 0:
                self.cursor.execute(
                    "UPDATE app_user SET password_hash = %s "
                    "WHERE id = %s",
                    (hashed, id)
                )
                self.db.commit()

                payload["message"] = "Password changed successfully"

        return self.__handle_response(email_error, phone_error, password_error, device_error, payload)

    # TODO
    def update_user(
            self,
            user_id,
            first_name: str = None,
            last_name: str = None,
            email_address: str = None,
            phone_number: str = None,
    ):
        email_error = 0
        phone_error = 0

        if (len(phone_number) == 8 or len(phone_number) == 9) and phone_number.isdigit():
            phone_number = "+373" + phone_number[-8:]

        if first_name is not None:
            self.__update_first_name(user_id, first_name)

        if last_name is not None:
            self.__update_last_name(user_id, last_name)

        if email_address is not None:
            self.__update_email(user_id, email_address)

        if phone_number is not None:
            self.__update_phone(user_id, phone_number)

        self.db.commit()

    # TODO: Add verification
    def buy_subscription(self, user_id, subscription_type: str):
        self.cursor.execute(
            "INSERT INTO user_subscription (user_id, subscription_id, created_at, removed_at)"
            "VALUES (%s, (SELECT id FROM subscription_type WHERE subscription_type_name = %s), %s)",
            (user_id, subscription_type, datetime.now())
        )
        self.db.commit()

# TODO: Add method for user update (update_user)
# TODO: Add subscription methods (buy subscription) check routes.py
# TODO: Create simu/ sime tables
# TODO: create methods for simu/ sime tables (check_student, check_elev, check_familie_monoparentala, check_familie_cu_multi_copii, check_personal_didactic, check_personal_medical)
                         # vezi sa adaugi verificarea ca in fiecare an sa mai faca o data check_user.

