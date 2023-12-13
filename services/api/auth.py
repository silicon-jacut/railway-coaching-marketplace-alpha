from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import check_password_hash
from pymongo import MongoClient
import os
from .old_users import create_user  # Make sure this import is correct based on your project structure

# -------------------------------------------------- Set up -------------------------------------------------- #

auth_blueprint = Blueprint('auth', __name__)

# ----------------------------------------- Authentication Functions ----------------------------------------- #

def validate_login(email: str, password: str) -> bool:
    user = users.find_one({'email': email})
    if user and check_password_hash(user['password'], password):
        return True
    return False

# --------------------------------------------- Blueprint Routes --------------------------------------------- #

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if validate_login(email, password):
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200

    return jsonify({'message': 'Invalid email or password'}), 401

@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    # Logic for user logout
    # You will need to handle token revocation here if required
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_blueprint.route('/reset-password', methods=['POST'])
def reset_password():
    # Logic for resetting password
    # Implementation depends on your application requirements
    return jsonify({'message': 'Password reset functionality not implemented'}), 501



# # --------------------------------------- Internal Authentication API --------------------------------------- #

# 🟠 Add this Blueprint to your Flask app in the main application file