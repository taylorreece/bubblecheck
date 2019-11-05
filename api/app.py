#!/usr/bin/env python3
import os
from flask import Flask
from flask import jsonify
from flask_login import current_user
from flask_login import LoginManager
from flask_login import login_user
from http import HTTPStatus
from models.user import User
from shared.bcjwt import bcjwt_secret
from shared.cognito import cognito
from shared.dynamodb import dynamodb

app = Flask(__name__)

# Set some application configuration from environment variables
app.config['DEBUG'] = True if os.environ.get('FLASK_DEBUG', 'false') == 'true' else False
app.config['ENV'] = 'development' if app.config['DEBUG'] else 'production'
app.config['THREADS_PER_PAGE'] = 2
app.config['CSRF_ENABLED'] = True
app.config['CSRF_SESSION_KEY'] = os.environ.get('CSRF_SESSION_KEY', 'secret')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret')
bcjwt_secret.set_secret(app.config['SECRET_KEY'])

# General AWS settings
app.config['AWS_REGION'] = os.environ.get('AWS_REGION')

# Set a couple of cognito-specific settings
app.config['COGNITO_URL'] = os.environ.get('COGNITO_URL')
app.config['COGNITO_CLIENT_ID'] = os.environ.get('COGNITO_CLIENT_ID')
cognito.init_app(app)

# Set up a couple of dynamo-specific settings
app.config['DYNAMO_ENDPOINT'] = os.environ.get('DYNAMO_ENDPOINT')
app.config['DYNAMO_TABLE'] = os.environ.get('DYNAMO_TABLE')
dynamodb.init_app(app)

# ===============================================================================
# Configure out login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = "You are not currently logged in."
@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        token = api_key.replace('Bearer ', '')
        return User.get_user_by_jwt(token=token)
    else:
        return None

@login_manager.user_loader
def load_user_session(email):
    return User(email)

# ===============================================================================
# Handle 500 errors gracefully
@app.errorhandler(500)
def internal_server_error(e):
    resp = jsonify(app="bubblecheck-flask", error="An unknown error occurred", success=False)
    resp.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return resp

# ===============================================================================
# Blueprint some endpoints
from routes import user_routes
from routes import course_routes
app.register_blueprint(user_routes.user_routes, url_prefix='/api/users')
app.register_blueprint(course_routes.course_routes, url_prefix='/api/courses')

# Quick hacky login
@app.route('/login')
def login():
    login_user(User('f3a41936-15e8-4da8-8a8f-5e22cac6ed6a'))
    return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0')