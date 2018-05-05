from flask import Blueprint
from flask import g
from flask import render_template
from flask import jsonify
from flask import request
from flask_login import login_required

from app.models import Course
from app.models import Section
from app.models import UserCoursePermission
from app import db

course_api_routes = Blueprint('course_api_routes', __name__)

@course_api_routes.route('/list', methods=['GET'])
@login_required
def listcourses():
    courses = g.user.courses
    return jsonify([course.serialize() for course in courses])

@course_api_routes.route('/add', methods=['POST'])
@login_required
def addcourse():
    request_data = request.get_json()
    new_course = Course(name=request_data['name'])
    for section_name in request_data['sections']:
        new_course.sections.append(Section(name=section_name))
    new_permission = UserCoursePermission(permission='owner', user=g.user, course=new_course) 
    db.session.add_all([new_course, new_permission])
    db.session.commit()
    db.session.refresh(new_course)
    return jsonify(new_course.serialize())
