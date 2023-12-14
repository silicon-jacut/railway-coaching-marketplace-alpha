from flask import Blueprint, request, jsonify
# from marshmallow import Schema, fields
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# -------------------------------------------------- Set up -------------------------------------------------- #

calendar_blueprint = Blueprint('calendar', __name__)

load_dotenv()

_client = MongoClient(os.getenv('PROTOTYPE_DB_CONNECTION_STRING'))
_db = _client[os.getenv('PROTOTYPE_DB_NAME')]
_users = _db['users']

# ----------------------------------------- Helper Functions/Objects ----------------------------------------- #



# ------------------------------------------------ Endpoints ------------------------------------------------- #

@calendar_blueprint.route('/coaches/calendar', methods=['POST'])
def coaches_calendar():
    print('hello world : ' + request.get_json())
    return jsonify({'Success in calendar update for '}), 501