from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app.models import User, Course, UserCourseAssociation, CoursePermissionEnum

db.create_all()
