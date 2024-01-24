from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask import jsonify, request

# import app
from __main__ import db, app, jwt


def init():
    pass


@app.route('/', methods=["GET"])
def hello_world():
    return jsonify(hello="World"), 200


# Endpoint for user signup
@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()

        first_name = data['first_name']
        last_name = data['last_name']
        phone_number = data['phone_number']
        password = data['password']
        email_address = data['email_address']
        device_name = data['device_name']
        birth_date = data['birth_date']

        response = db.register(phone_number=phone_number, password=password, email_address=email_address,
                               first_name=first_name, last_name=last_name, device_name=device_name,
                               birth_date=birth_date)

        return jsonify(response), 201


# Endpoint for user login
# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    phone_number = data['phone_number']
    password = data['password']

    response = db.login(credential=phone_number, password=password)

    if response['type'] == 'success':
        user_id = response["data"]["user_id"]
        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)
        return jsonify(access_token=access_token, refresh_token=refresh_token, response=response), 200
    return jsonify(response), 401


# We are using the `refresh=True` options in jwt_required to only allow
# refresh tokens to access this route.
@app.route("/refresh", methods=["GET"])
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
    return db.get_user_by_id(current_user), 200


@app.route('/update_user_information', methods=['PUT'])
@jwt_required()
def update_user_information():
    if request.method == 'PUT':
        current_user = get_jwt_identity()
        data = request.get_json()

        first_name = data['first_name']
        last_name = data['last_name']
        phone_number = data['phone_number']
        email_address = data['email_address']
        
        # TODO: [Update new user data in database]
        pass

@app.route('/update_password', methods=['PUT'])
@jwt_required()
def update_password():
    if request.method == 'PUT':
        current_user = get_jwt_identity()
        data = request.get_json()

        user_id = data['user_id']
        old_password = data['old_password']
        new_password = data['new_password']

        change_password_response = db.change_password(user_id=user_id, old_password=old_password, new_password=new_password)

        if change_password_response['type'] == 'success':
            return jsonify(change_password_response), 200
        else:
            return jsonify(change_password_response), 401


@app.route('/buy_subscription', methods=['POST'])
@jwt_required()
def subscription_manager():
    if request.method == 'POST':
        user_id = get_jwt_identity()

        data = request.get_json()
        subscription_type = data['subscription_type']
        payment_method = data['payment_method']
        payment_amount = data['payment_amount']

        # Todo: [Buy subscription] // Corneliu
        # buy_subscription_response = db.buy_subscription(user_id=user_id, subscription_type=subscription_type)



@app.route('/device_manager', methods=['GET', 'POST'])
@jwt_required()
def device_manager():
    if request.method == 'GET':
        current_user = get_jwt_identity()
        return jsonify({'message': 'Device manager', 'user_id': current_user}), 200
    elif request.method == 'POST':
        pass


@app.route('/payment_information', methods=['GET', 'POST'])
@jwt_required()
def payment_information():
    if request.method == 'GET':
        current_user = get_jwt_identity()
        return jsonify({'message': 'Payment information', 'user_id': current_user}), 200
    elif request.method == 'POST':
        pass


@app.route('/payment_manager', methods=['GET', 'POST'])
@jwt_required()
def payment_manager():
    if request.method == 'GET':
        current_user = get_jwt_identity()
        return jsonify({'message': 'Payment manager', 'user_id': current_user}), 200
    elif request.method == 'POST':
        pass
