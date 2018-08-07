from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import request
from flask import Response
from flask_login import current_user
from flask_login import login_required
from functools import wraps
from http import HTTPStatus
from werkzeug import MultiDict

from bubblecheck.forms import CourseForm
from bubblecheck.models import Course
from bubblecheck.models import CoursePermissionEnum
from bubblecheck.models import Section
from bubblecheck.models import UserCoursePermission
from bubblecheck import db

course_api_routes = Blueprint('course_api_routes', __name__)

def course_permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_permission = (UserCoursePermission.query
                                .filter(UserCoursePermission.courses_id==kwargs['course_id'])
                                .filter(UserCoursePermission.users_id==current_user.id)
                                .first()
                                .permission.value)
            required_permission = CoursePermissionEnum[permission].value
            if required_permission > user_permission:
                resp = jsonify(error='You do not have sufficient permissions to access this resource.', success=False)
                resp.status_code = HTTPStatus.UNAUTHORIZED
                return resp
            else:
                return f(*args, **kwargs)
        return decorated_function
    return decorator

@course_api_routes.route('/list', methods=['GET'])
@login_required
def list_courses():
    return jsonify(courses=[course.toJSON() for course in current_user.courses], success=True)

@course_api_routes.route('/<course_id>', methods=['GET'])
@login_required
@course_permission_required('view')
def get_course(course_id):
    course = Course.query.get(course_id)
    return jsonify(course=course.toJSON(show_users=True, show_exams=True, show_sections=True), success=True)

@course_api_routes.route('/update/<course_id>', methods=['POST'])
@login_required
@course_permission_required('edit')
def update_course(course_id):
    request_data = request.get_json()
    course = Course.query.get(course_id)
    course.name = request_data['name']
    db.session.add(course)
    db.session.commit()
    db.session.refresh(course)
    return jsonify(course=course.toJSON(show_users=True, show_exams=True, show_sections=True), success=True)

@course_api_routes.route('/add', methods=['POST'])
@login_required
def add_course():
    request_data = request.get_json()
    form = CourseForm(MultiDict(request_data))
    if form.validate():
        new_course = Course(name=request_data['name'])
        for section_name in request_data['sections']:
            new_course.sections.append(Section(name=section_name))
        new_permission = UserCoursePermission(permission='own', user=current_user, course=new_course) 
        db.session.add_all([new_course, new_permission])
        db.session.commit()
        db.session.refresh(new_course)
        return jsonify(course=new_course.toJSON(show_sections=True), success=True)
    else:
        resp = jsonify(error="Form validation errors", errors=form.errors, success=False)
        resp.status_code = HTTPStatus.BAD_REQUEST
        return resp

@course_api_routes.route('/<course_id>', methods=['DELETE'])
@login_required
@course_permission_required('own')
def delete_course(course_id):
    course = Course.query.get(course_id)
    course.active = False
    db.session.add(course)
    db.session.commit()
    return jsonify(message="Successfully deleted course", success=True)

@course_api_routes.route('/<course_id>/section/add', methods=['POST'])
@login_required
@course_permission_required('edit')
def course_section_add(course_id):
    request_data = request.get_json()
    new_section = Section(name=request_data['name'])
    course = Course.query.get(course_id)
    course.sections.append(new_section)
    db.session.add(course)
    db.session.commit()
    db.session.refresh(new_section)
    return jsonify(section=new_section.toJSON(), success=True)

@course_api_routes.route('/<course_id>/section/<section_id>/update', methods=['POST'])
@login_required
@course_permission_required('edit')
def course_section_update(course_id, section_id):
    request_data = request.get_json()
    section = Section.query.get(section_id)
    if section and section.courses_id == course_id:
        section.name = request_data['name']
        db.session.add(section)
        db.session.commit()
        db.session.refresh(section)
        return jsonify(section=section.toJSON(), success=True)
    else:
        resp = jsonify(error='No such courseid/sessionid combination found.', success=False)
        resp.status_code = HTTPStatus.BAD_REQUEST
        return resp

@course_api_routes.route('/<course_id>/section/<section_id>', methods=['DELETE'])
@login_required
@course_permission_required('edit')
def course_section_delete(course_id, section_id):
    section = Section.query.get(section_id)
    if section and section.courses_id == course_id:
        section.active = False
        db.session.add(section)
        db.session.commit()
        return jsonify(message="Successfully deleted section.", success=True)
    else:
        resp = jsonify(error='No such courseid/sessionid combination found.', success=False)
        resp.status_code = HTTPStatus.BAD_REQUEST
        return resp