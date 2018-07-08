import os
from flask import Flask, g, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import current_user
from flask_login import LoginManager

app = Flask(__name__)

if os.path.isfile(os.path.join(os.path.dirname(__file__), '..', 'config', 'production.py')):
    app.logger.info("Using production configuration")
    app.config.from_object('config.production')
else:
    app.logger.info("Using testing configuration")
    app.config.from_object('config.testing')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from bubblecheck.models import User
from bubblecheck.models import Course
from bubblecheck.models import Exam
from bubblecheck.models import Section

# ===============================================================================
# Configure out login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"
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
# Map out some generally non-API routes:
from bubblecheck.views import default_view_routes
from bubblecheck.views import user_views
app.register_blueprint(default_view_routes)
app.register_blueprint(user_views.user_web_routes, url_prefix='/user')

# ===============================================================================
# Define our API endpoints:
from bubblecheck.api import course_api
from bubblecheck.api import exam_api
from bubblecheck.api import user_api
app.register_blueprint(course_api.course_api_routes, url_prefix='/api/course')
app.register_blueprint(exam_api.exam_api_routes, url_prefix='/api/exam')
app.register_blueprint(user_api.user_api_routes, url_prefix='/api/user')
