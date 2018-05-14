from flask import Blueprint
from flask import render_template
from flask import jsonify

from app.decorators import login_required_api
from app.models import Course
from app import db

course_api_routes = Blueprint('course_api_routes', __name__)

@course_api_routes.route('/list')
@login_required_api
def listcourses():
    courses = G.user.courses
    return jsonify(courses=[course.serialize for course in courses])
