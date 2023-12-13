from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash
from pymongo.errors import DuplicateKeyError
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os

# -------------------------------------------------- Set up -------------------------------------------------- #

users_blueprint = Blueprint('users', __name__)

load_dotenv()

_client = MongoClient(os.getenv('PROTOTYPE_DB_CONNECTION_STRING'))
_db = _client[os.getenv('PROTOTYPE_DB_NAME')]
_users = _db['users']

# ----------------------------------------- Helper Functions/Objects ----------------------------------------- #

def create_user(password : str, email : str,  is_coach : bool, first_name = None, last_name = None):
    hashed_password = generate_password_hash(password)
    user = {
        'firstName': first_name,
        'lastName': last_name,
        'email': email,
        'password': hashed_password,
        'isCoach': is_coach,
    }
    
    try:
        _users.insert_one(user)
        return jsonify({'message': 'User created successfully'}), 201
    except DuplicateKeyError:   # Check if that works 🟠
        return jsonify({'Error': 'User with given email already exists'}), 409
    
def update_coach_profile(title, tags, description):

    _users.update_one({})
    return jsonify({'message': 'User created successfully'}), 201
    
def get_user_by_id(user_id : str):
    # Retrieve user by user_id
    user = _users.find_one({'_id': user_id})
    return user

def get_user_by_email(email : str):
    # Retrieve user by user_id
    user = _users.find_one({'email': email})
    return user

def update_user(email : str, update_data : dict):
    # Update user information
    _users.update_one({'email': email}, {'$set': update_data})
    return get_user_by_id(email)

# def delete_user(user_id : str|ObjectId):
#     # Delete user from database
#     _users.delete_one({'_id': user_id})


# ------------------------------------------------ Endpoints ------------------------------------------------- #

@users_blueprint.route('/create-user', methods=['POST'])
def api_create_user():
    # Extract user data from request
    data = request.get_json()
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')
    password = data.get('password')

    return create_user(password, email, is_coach=False, first_name=first_name, last_name=last_name)

@users_blueprint.route('/coaches/create-user', methods=['POST'])
def api_coaches_create_user():
    # Extract user data from request
    data = request.get_json()
    # first_name = data.get('firstName')
    # last_name = data.get('lastName')
    # email = data.get('email')
    # password = data.get('password')

    data_items = first_name, last_name, email, password = data.get('firstName'), data.get('lastName'), data.get('email'), data.get('password')

    if len(data_items) < 4:
        return jsonify({'Error':'All fields required.'}), 403
    # create_user(password, email, is_coach=True, first_name=first_name, last_name=last_name)
    
    # return create_user(password, email, is_coach=True, first_name=first_name, last_name=last_name)

    _users.insert_one({'firstName':first_name, 'lastName':last_name, 'email': email, 'hPassword': generate_password_hash(password)})

    return jsonify({'message':'Success in creating coach account.'}), 200

@users_blueprint.route('/coaches/edit-profile')
def api_coaches_edit_profile():
    data = request.get_json()
    data_items = title, tags, description = data['title'], data['tags'], data['description']

    
    return jsonify({'message':'Success in updating profile in the database.'}), 200



@users_blueprint.route('/get_user/<user_email>', methods=['GET'])
def api_get_user(user_email):
    # Retrieve user details
    user = get_user_by_email(user_email)
    if user:
        return jsonify(user), 200
    return jsonify({'message': 'User not found'}), 404

@users_blueprint.route('/modify_user')
def api_modify_user():
    data = request.get_json()
    db_response = update_user(data['email'])
    return jsonify({'message':'Updated user data successfully.'}), 200