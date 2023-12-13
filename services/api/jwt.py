from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, set_refresh_cookies, set_access_cookies, create_access_token, create_refresh_token
from pymongo import MongoClient
import os

# -------------------------------------------------- Set up -------------------------------------------------- #

service_blueprint = Blueprint('jwt', __name__)

# ----------------------------------------- Helper Functions/Objects ----------------------------------------- #



# ------------------------------------------------ Endpoints ------------------------------------------------- #

@service_blueprint.route('/refresh', methods=['GET'])
@jwt_required(refresh=True)
def refresh():
    # Creates a HTTP response
    response = make_response({'message':'Access and refresh JWTs re-created successfully'})

    # Creates new JWTs
    access_jwt = create_access_token(fresh=False)
    refresh_jwt = create_refresh_token()

    # Set them as cookies
    set_access_cookies(response, access_jwt)
    set_refresh_cookies(response, refresh_jwt)
    return response, 200