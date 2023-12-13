from flask import Flask, jsonify
# from config import Config
# from sanitize import UniversalSanitizerMiddleware
from services.web_views.routes import routes_blueprint
from services.api.users import users_blueprint
import os

from pymongo import MongoClient

# client = MongoClient('mongodb+srv://timothee-oliveau:Y6OXjsKKBjKKqAvc@coachingmarketplace.h2hzjxp.mongodb.net/?retryWrites=true&w=majority')
# client = MongoClient(os.getenv('PROTOTYPE_DB_CONNECTION_STRING'))

# db = client[os.getenv('PROTOTYPE_DB_NAME')]

# db['users'].insert_one({'ouaou':'de feu env env'})

app = Flask(__name__)

# app.config.from_object(Config)

# # Apply the Universal Sanitizer Middleware
# app.wsgi_app = UniversalSanitizerMiddleware(app.wsgi_app)

# # Import routes and other parts of your application here
# from your_application import routes, models, etc.

app.register_blueprint(users_blueprint, url_prefix='/api')

app.register_blueprint(routes_blueprint, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
