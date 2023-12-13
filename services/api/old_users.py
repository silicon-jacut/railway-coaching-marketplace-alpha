from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
import os

# -------------------------------------------------- Set up -------------------------------------------------- #

users_blueprint = Blueprint('users', __name__)

_client = MongoClient(os.getenv('PROTOTYPE_DB_CONNECTION_STRING'))
_db = _client[os.getenv('POTOTYPE_DB_NAME')]
_users = _db['users']

# ----------------------------------------- User Management Functions ---------------------------------------- #

def create_user(username, password, email):
    hashed_password = generate_password_hash(password)
    user = {
        'username': username,
        'email': email,
        'password': hashed_password
    }
    
    try:
        _users.insert_one(user)
        return {'message': 'User created successfully'}, 201
    except DuplicateKeyError:   # Check if that works 🟠
        return {'message': 'User with given email already exists'}, 409

def get_user(user_id : str):
    # Retrieve user by user_id
    user = _users.find_one({'_id': user_id})
    return user

def get_user_by_email(email : str):
    user = _users.find_one({'email': email})
    return user

def update_user(user_id : str, update_data : dict):
    # Update user information
    _users.update_one({'_id': user_id}, {'$set': update_data})
    return get_user(user_id)

def delete_user(user_id : str|ObjectId):
    # Delete user from database
    _users.delete_one({'_id': user_id})

def validate_user(username : str, email : str):
    # Add any logic if wanted
    # Some of it is already done in sanitize.py, middleware.
    return True

def check_user_password(email : str, password : str):
    user = _users.find_one({'email': email})
    if user and check_password_hash(user['password'], password):
        return True
    return False

# --------------------------------------- User Blueprint Routes -------------------------------------------- #

from flask import request

@users_blueprint.route('/create_user', methods=['POST'])
def api_create_user():
    # Extract user data from request
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Validate and create user
    if validate_user(username, email):
        user = create_user(username, email, password)
        return jsonify({'message': 'User created', 'user': user}), 201

    return jsonify({'message': 'Invalid user data'}), 400

@users_blueprint.route('/get_user/<user_id>', methods=['GET'])
def api_get_user(user_id):
    # Retrieve user details
    user = get_user(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({'message': 'User not found'}), 404

@users_blueprint.route('/update_user/<user_id>', methods=['PUT'])
def api_update_user(user_id):
    # Extract update data from request
    update_data = request.get_json()

    # Update user
    if update_user(user_id, update_data):
        return jsonify({'message': 'User updated'}), 200
    return jsonify({'message': 'User not found or update failed'}), 400

@users_blueprint.route('/delete_user/<user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    # Delete the user
    if delete_user(user_id):
        return jsonify({'message': 'User deleted'}), 200
    return jsonify({'message': 'User not found or delete failed'}), 400

# 🟠 Add this Blueprint to your Flask app in the main application file
