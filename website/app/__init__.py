from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models import Course
from app.models import CoursePermissionEnum
from app.models import Section
from app.models import User
from app.models import UserCoursePermission

from app import views

from app.api.user import user_api_routes
from app.api.course import course_api_routes

app.register_blueprint(user_api_routes, url_prefix='/api/user')
app.register_blueprint(course_api_routes, url_prefix='/api/course')
