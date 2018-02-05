from flask import Flask
from flask import request
from flask import session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user_web_routes.login"

from app.models import User

from app import views

# Regiser web blueprints
from app.views.default import default_web_views
app.register_blueprint(default_web_views)
from app.views.user import user_web_routes
app.register_blueprint(user_web_routes, url_prefix='/user')

# Register API Blueprints
from app.api.course import course_api_routes
app.register_blueprint(course_api_routes, url_prefix='/api/course')
from app.api.exam import exam_api_routes
app.register_blueprint(exam_api_routes, url_prefix='/api/exam')
from app.api.user import user_api_routes
app.register_blueprint(user_api_routes, url_prefix='/api/user')

# NOTE TO SELF:
# When we implement login, we'll just need to set session['jwt_token'] to some valid token
# EZPZ
@login_manager.request_loader
def load_user(user_id):
    token = None
    if 'jwt_token' in session:
        token = str(session['jwt_token'])
    elif request.authorization:
        token = request.authorization.username
    if token:
        return User().get_user_by_jwt(token)
    else:
        return None
