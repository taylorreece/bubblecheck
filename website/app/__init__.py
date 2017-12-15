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
