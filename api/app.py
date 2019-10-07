#!/usr/bin/env python3
import os
from database import db
from flask import Flask, g, request, session, jsonify, render_template
from flask_migrate import Migrate
from flask_login import current_user
from flask_login import LoginManager
from http import HTTPStatus

app = Flask(__name__)

# Set some application configuration from environment variables
app.config['DEBUG'] = True if os.environ.get('FLASK_DEBUG', 'false') == 'true' else False
app.config['ENV'] = 'development' if app.config['DEBUG'] else 'production'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DATABASE_CONNECT_OPTIONS'] = {}
app.config['THREADS_PER_PAGE'] = 2
app.config['CSRF_ENABLED'] = True
app.config['CSRF_SESSION_KEY'] = os.environ.get('CSRF_SESSION_KEY', 'secret')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret')

db.init_app(app)
migrate = Migrate(app, db)

from models import User
from models import Course
from models import Exam
from models import Section
from models import StudentExam

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
def load_user_session(user_id):
    return User.query.get(user_id)

# ===============================================================================
# Map out some non-API routes (just for static front-end stuff)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        import requests
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("dist/index.html")

# ===============================================================================
# Handle 500 errors gracefully
@app.errorhandler(500)
def internal_server_error(e):
    resp = jsonify(error="An unknown error occurred", success=False)
    resp.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return resp

# ===============================================================================
# Define our API endpoints:
from routes import course_api
from routes import user_api
app.register_blueprint(course_api.course_api_routes, url_prefix='/api/course')
app.register_blueprint(user_api.user_api_routes, url_prefix='/api/user')

if __name__ == '__main__':
    app.run(host='0.0.0.0')