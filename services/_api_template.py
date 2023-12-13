from flask import Blueprint, request, jsonify
# from marshmallow import Schema, fields
from pymongo import MongoClient
import os

# -------------------------------------------------- Set up -------------------------------------------------- #

NAMEOFTHISFILE_blueprint = Blueprint('NAMEOFTHISFILE', __name__)

_client = MongoClient(os.getenv('PROTOTYPE_DB_CONNECTION_STRING'))
_db = _client[os.getenv('PROTOTYPE_DB_NAME')]
_NAMEOFTHISFILE = _db['NAMEOFTHISFILE']

# ----------------------------------------- Helper Functions/Objects ----------------------------------------- #



# ------------------------------------------------ Endpoints ------------------------------------------------- #

@service_blueprint.route('/', methods=['GET'])
def _():
    return '', 501