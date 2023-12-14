from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash
from pymongo.errors import DuplicateKeyError
import json
import openai
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
from time import sleep
import os

# -------------------------------------------------- Set up -------------------------------------------------- #

browse_coaches_blueprint = Blueprint('browse_coaches', __name__)

load_dotenv()

_client = MongoClient(os.getenv('PROTOTYPE_DB_CONNECTION_STRING'))
_db = _client[os.getenv('PROTOTYPE_DB_NAME')]
_users = _db['users']

openai.api_key = os.getenv("OPENAI_API_KEY")

def prompt(prompt, model='gpt-4'):

    print('prompt() - prompting')

    messages_query = []
    prompt_as_messages = False
    if type(prompt) == list:
        prompt_as_messages = True
        messages_query = prompt
        print('prompt() - type prompt == List')

    if not prompt_as_messages:
        messages_query.append({"role": "user", "content": prompt})
        print('prompt() - not prompt_as_messages:')

    # Handling usage limit error.
    for i in range(10):
        print('prompt() - starting loop')
        try:
            print('prompt() - Try')
            response = openai.chat.completions.create(model=model, messages=messages_query)
            print('prompt() - tried')
            break
        # Handling usage limit error.
        except openai.RateLimitError as e:
            print('prompt() - except')
            print(f"prompt() - Rate limit exceeded. Retrying in {5**i} seconds.")
            sleep(5 ** i)
    # print('response : ' + str(response))
    answer = str(response.choices[0].message.content)

    return answer

def dict_search(dict_list: list, key, wanted_value):
    for d in dict_list:
        if d.get(key) == wanted_value:
            print("Found:", d)
            break

# ----------------------------------------- Helper Functions/Objects ----------------------------------------- #

# ------------------------------------------------ Endpoints ------------------------------------------------- #

@browse_coaches_blueprint.route('/', methods=['POST'])
def api_create_user():
    data = request.get_json()

    coaches = _users.find({'isCoach':True})

    new_list = []
    for coach in coaches:
        coach['_id'] = str(coach['_id'])
        new_list.append(coach)
    coaches = new_list

    response = prompt('Someone is searching for the perfect match for a coach. They searched with the following terms : ' + str(data) + '\n\n\n Here are a list of coaches : ' + str(coaches) + '\n\n\nIn a json format, rank the coaches in a perfect order for this person, add a "comment" section to each coach as to why they could be the best match for this client. Only answer with the Json list [{},{},{}]. Answer only in this format : [{rank: 1; firstName: Firstname, email: email@email.com, comment: comment},]')
    try:
        response = json.loads(response)
        # no_prompt = False
    except json.decoder.JSONDecodeError:
        return jsonify({'message':'Error decoding the response, try again'})
    
    final_ranked_coach_list = []

    # if no_prompt == False:

    for ranked_coach in response:

        corresponding_db_coach_dict = dict_search(coaches, 'firstName', ranked_coach['firstName'])

        if corresponding_db_coach_dict is not None:
            ranked_coach['tags'] = corresponding_db_coach_dict['tags']
            ranked_coach['personality'] = corresponding_db_coach_dict['personality']
            ranked_coach['firstName'] = corresponding_db_coach_dict['firstName']
            ranked_coach['lastName'] = corresponding_db_coach_dict['lastName']
            ranked_coach['title'] = corresponding_db_coach_dict['title']
            # ranked_coach['hourlyRate'] = corresponding_db_coach_dict['tags']
            # ranked_coach['description'] = corresponding_db_coach_dict['tags']
            
            print('rkdcch' + ranked_coach)
            print('FRCL' + final_ranked_coach_list)

            final_ranked_coach_list.append(ranked_coach)
        else:
            print(f"Coach with name {ranked_coach['firstName']} not found in database.")

        print('\n\n\n' + str(json.dumps(new_list, indent=4)) + '\n\n\n')

    return jsonify({'message': 'browse successful', 'coaches': new_list}), 200

    # return create_user(password, email, is_coach=False, first_name=first_name, last_name=last_name)