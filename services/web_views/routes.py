from flask import render_template, Blueprint

routes_blueprint = Blueprint('routes', __name__)

# Homepage route
@routes_blueprint.route('/')
def index():
    return render_template('site/clients/index.html')

@routes_blueprint.route('/coaches')
def coaches_index():
    return render_template('site/coaches/index.html')

# Login page route
@routes_blueprint.route('/login')
def login():
    return render_template('auth/login.html')

# Registration page route
@routes_blueprint.route('/register')
def register():
    return render_template('auth/register.html')

@routes_blueprint.route('/coaches/register')
def coaches_register():
    return render_template('auth/coaches-register.html')

@routes_blueprint.route('/clients/emailsim')
def clients_emailsim():
    return render_template('emails/clients.html')

@routes_blueprint.route('/coaches/emailsim')
def coaches_emailsim():
    return render_template('emails/coaches.html')

@routes_blueprint.route('/my-page')
def coaches_dashboard():
    return render_template('platform/coaches/dashboard/my-page.html')

# Change password route
@routes_blueprint.route('/change-password')
def change_password():
    return render_template('auth/change_password.html')

# User profile route
@routes_blueprint.route('/profile')
def profile():
    return render_template('platform/profile.html')

# Settings page route
@routes_blueprint.route('/settings')
def settings():
    return render_template('platform/settings.html')
