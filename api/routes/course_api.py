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

from forms import CourseForm
from models import Course
from models import CoursePermissionEnum
from models import Exam
from models import Section
from models import StudentExam
from models import UserCoursePermission
from database import db

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

@course_api_routes.route('/', methods=['GET'])
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

###############################################################################
# Section Endpoints
@course_api_routes.route('/<course_id>/section/add', methods=['POST'])
@login_required
@course_permission_required('edit')
def add_section(course_id):
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
def update_section(course_id, section_id):
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
def delete_section(course_id, section_id):
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

###############################################################################
# Exam Endpoints
@course_api_routes.route('/<course_id>/exams', methods=['GET'])
@login_required
@course_permission_required('view')
def list_exams(course_id):
    course = Course.query.get(course_id)
    return jsonify(exams=[exam.toJSON() for exam in course.exams], success=True)

@course_api_routes.route('/<course_id>/exam/<exam_id>', methods=['GET'])
@login_required
@course_permission_required('view')
def get_exam(course_id, exam_id):
    exam = Exam.query.get(exam_id)
    return jsonify(exam=exam.toJSON(show_student_exams=True), success=True)

@course_api_routes.route('/<course_id>/exam/add', methods=['POST'])
@login_required
@course_permission_required('edit')
def add_exam(course_id):
    request_data = request.get_json()
    new_exam = Exam(
        name=request_data['name'],
        exam_format=request_data['exam_format'])
    course = Course.query.get(course_id)
    course.exams.append(new_exam)
    db.session.add(course)
    db.session.commit()
    db.session.refresh(new_exam)
    return jsonify(exam=new_exam.toJSON(), success=True)

@course_api_routes.route('/<course_id>/exam/<exam_id>/update', methods=['POST'])
@login_required
@course_permission_required('edit')
def update_exam(course_id, exam_id):
    request_data = request.get_json()
    exam = Exam.query.get(exam_id)
    if exam and exam.courses_id == course_id:
        if 'name' in request_data:
            exam.name = request_data['name']
        if 'exam_format' in request_data:
            exam.exam_format = request_data['exam_format']
        db.session.add(exam)
        db.session.commit()
        db.session.refresh(exam)
        return jsonify(exam=exam.toJSON(), success=True)
    else:
        resp = jsonify(error='No such courseid/examid combination found')
        resp.status_code = HTTPStatus.BAD_REQUEST
        return resp

@course_api_routes.route('/<course_id>/exam/<exam_id>', methods=['DELETE'])
@login_required
@course_permission_required('edit')
def delete_exam(course_id, exam_id):
    request_data = request.get_json()
    exam = Exam.query.get(exam_id)
    if exam and exam.courses_id == course_id:
        exam.active = False
        db.session.add(exam)
        db.session.commit()
        return jsonify(message="Successfully deleted exam.", success=True)
    else:
        resp = jsonify(error='No such courseid/examid combination found.', success=False)
        resp.status_code = HTTPStatus.BAD_REQUEST
        return resp

###############################################################################
# Student Exam Endpoints
@course_api_routes.route('/<course_id>/exam/<exam_id>/student_exam', methods=['POST'])
@login_required
@course_permission_required('edit')
def add_student_exam(course_id, exam_id):
    request_data = request.get_json()
    new_student_exam = StudentExam(answers = request_data.get('answers'))
    exam = Exam.query.get(exam_id)
    if exam and exam.courses_id == course_id:
        exam.student_exams.append(new_student_exam)
        db.session.add(exam)
        db.session.commit()
        db.session.refresh(new_student_exam)
        return jsonify(student_exam=new_student_exam.toJSON(), success=True)

@course_api_routes.route('/<course_id>/exam/<exam_id>/student_exam/<student_exam_id>', methods=['POST'])
@login_required
@course_permission_required('edit')
def update_student_exam(course_id, exam_id, student_exam_id):
    request_data = request.get_json()
    student_exam = StudentExam.query.get(student_exam_id)
    if student_exam and student_exam.exams_id == exam_id:
        if 'answers' in request_data:
            student_exam.answers = request_data['answers']
        db.session.add(student_exam)
        db.session.commit()
        db.session.refresh(student_exam)
        return jsonify(exam=student_exam.toJSON(), success=True)
    else:
        resp = jsonify(error='No such courseid/examid combination found')
        resp.status_code = HTTPStatus.BAD_REQUEST
        return resp

@course_api_routes.route('/<course_id>/exam/<exam_id>/student_exam/<student_exam_id>', methods=['DELETE'])
@login_required
@course_permission_required('edit')
def delete_student_exam(course_id, exam_id, student_exam_id):
    student_exam = StudentExam.query.get(student_exam_id)
    if student_exam and student_exam.exams_id == exam_id:
        student_exam.active = False
        db.session.add(student_exam)
        db.session.commit()
        return jsonify(message="Successfully deleted student_exam.", success=True)
    else:
        resp = jsonify(error='No such courseid/examid/student_exam combination found.', success=False)
        resp.status_code = HTTPStatus.BAD_REQUEST
        return resp
