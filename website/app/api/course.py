from flask import Blueprint
from flask import g
from flask import render_template
from flask import jsonify
from flask_login import login_required

from app.models import Course
from app import db

course_api_routes = Blueprint('course_api_routes', __name__)

@course_api_routes.route('/list')
@login_required
def listcourses():
    courses = g.user.courses
    return jsonify([course.serialize() for course in courses])
