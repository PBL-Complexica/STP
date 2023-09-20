DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public;

CREATE TABLE app_user (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    password_hash VARCHAR NOT NULL,
    birthday DATE,
    create_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE email_address (
    email_address_id SERIAL PRIMARY KEY,
    email_address VARCHAR(50) NOT NULL,
    create_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_email (
    user_email_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES app_user(user_id),
    email_address_id INTEGER NOT NULL REFERENCES email_address(email_address_id),
    create_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    remove_ts TIMESTAMP NOT NULL DEFAULT 2100-01-01
);

CREATE TABLE phone_number (
    phone_number_id SERIAL PRIMARY KEY,
    phone_number VARCHAR(50) NOT NULL,
    create_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_phone (
    user_phone_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES app_user(user_id),
    phone_number_id INTEGER NOT NULL REFERENCES phone_number(phone_number_id),
    create_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    remove_ts TIMESTAMP NOT NULL DEFAULT 2100-01-01
);

CREATE TABLE device (
    device_id SERIAL PRIMARY KEY,
    device_name VARCHAR(50) NOT NULL,
    device_sn VARCHAR NOT NULL,
    create_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_device (
    user_device_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES app_user(user_id),
    device_id INTEGER NOT NULL REFERENCES device(device_id),
    create_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    remove_ts TIMESTAMP NOT NULL DEFAULT 2100-01-01
);

CREATE TABLE category (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL,
    create_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_category (
    user_category_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES app_user(user_id),
    category_id INTEGER NOT NULL REFERENCES category(category_id),
    create_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    remove_ts TIMESTAMP NOT NULL DEFAULT 2100-01-01
);

CREATE TABLE subscription_type (
    subscription_type_id SERIAL PRIMARY KEY,
    subscription_type_name VARCHAR(50) NOT NULL,
    create_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE subscription (
    subscription_id SERIAL PRIMARY KEY,
    subscription_type_id INTEGER NOT NULL REFERENCES subscription_type(subscription_type_id),
    subscription_name VARCHAR(50) NOT NULL,
    valid_from TIMESTAMP NOT NULL,
    create_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_subscription (
    user_subscription_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES app_user(user_id),
    subscription_id INTEGER NOT NULL REFERENCES subscription(subscription_id),
    create_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    remove_ts TIMESTAMP NOT NULL DEFAULT 2100-01-01
);
