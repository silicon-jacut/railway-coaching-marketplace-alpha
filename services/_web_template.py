# _web_views_template.py

from flask import Blueprint, render_template, request, jsonify

# Initialize Blueprint for web views
web_views_blueprint = Blueprint('you_can_set_this_blueprint_name_as_the_file_name_but_without_dotpy_though_', __name__)

# -------------------------------------------- Web Page Routes -------------------------------------------- #

@web_views_blueprint.route('/')
def index():
    """
    Render the main index page.
    """
    # Logic to gather data to display on the index page, if any
    return render_template('index.html')

@web_views_blueprint.route('/about')
def about():
    """
    Render the 'About' page.
    """
    # Logic for the 'About' page
    return render_template('about.html')

# --------------------------------------- API Endpoints for Web Views -------------------------------------- #

@web_views_blueprint.route('/api/data', methods=['GET', 'POST'])
def api_data():
    """
    API endpoint for web view specific data.
    """
    # API logic to serve data to the web view
    return jsonify({"message": "Data for web view"})

# 🟠 Register this Blueprint in your Flask app in the main application file
