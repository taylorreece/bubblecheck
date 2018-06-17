from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import request
from flask import Response
from flask_login import current_user
from flask_login import login_required
from functools import wraps
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
            user_permission = (db.session.query(UserCoursePermission)
                                .filter(UserCoursePermission.courses_id==kwargs['course_id'])
                                .filter(UserCoursePermission.users_id==current_user.id)
                                .first()
                                .permission.value)
            print(permission, type(permission))
            required_permission = CoursePermissionEnum[permission].value
            if required_permission > user_permission:
                return jsonify(error='You do not have sufficient permissions to access this resource.')
            else:
                return f(*args, **kwargs)
        return decorated_function
    return decorator

@course_api_routes.route('/list', methods=['GET'])
@login_required
def list_courses():
    return jsonify(courses=[course.toJSON() for course in current_user.courses])

@course_api_routes.route('/get/<int:course_id>', methods=['GET'])
@login_required
@course_permission_required('view')
def get_course(course_id):
    course = db.session.query(Course).filter(Course.id==course_id).first()
    return jsonify(course.toJSON(show_users=True, show_exams=True, show_sections=True))

@course_api_routes.route('/add', methods=['POST'])
@login_required
def addcourse():
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
        return jsonify(new_course.toJSON(show_sections=True))
    else:
        resp = jsonify(msg="Form validation errors", errors=form.errors)
        resp.status_code = 400
        return resp