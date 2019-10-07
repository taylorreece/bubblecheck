from flask_login import UserMixin
from flask_login import current_user
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from database import db
import datetime
import enum
import json
import jwt
import uuid

def generate_uuid():
   return str(uuid.uuid4())

# ==============================================================================
# Define a base model for other database tables to inherit
class Base(db.Model):
    __abstract__  = True
    id = db.Column(db.Text(), primary_key=True, default=generate_uuid)
    created  = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.current_timestamp())
    modified = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    active   = db.Column(db.Boolean(), nullable=False, default=True)

# ==============================================================================
class User(UserMixin, Base):
    __tablename__ = 'users'
    email = db.Column(db.Text(), nullable=False, index=True, unique=True)
    teachername = db.Column(db.Text(), nullable=False)
    password = db.Column(db.Text(), nullable=False)
    is_admin = db.Column(db.Boolean(), nullable=False, default=False)
    public_uuid = db.Column(db.Text(), nullable=False, index=True, default=generate_uuid, unique=True)

    courses = relationship(
        'Course',
        secondary='users_courses_permissions',
        secondaryjoin="and_(UserCoursePermission.courses_id==Course.id, Course.active)",
        back_populates='users'
    )
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def create_jwt(self):
        return jwt.encode(
            payload={
                'email': self.email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=72)
            }, 
            key=self.password,
            algorithm='HS256'
        ).decode()

    def get_user_by_jwt(token):
        try:
            decoded_token = jwt.decode(token, verify=False)
            u = User.query.filter(User.email==decoded_token['email']).one_or_none()
            if u and jwt.decode(token, u.password, algorithms=['HS256']):
                return u
            else:
                return None
        except jwt.exceptions.DecodeError as e:
            return None

    def __repr__(self):
        return '<User %r (id=%r)>' % (self.email, self.id)

    def toJSON(self):
        return {
            'email':        self.email,
            'teachername':  self.teachername,
            'id':           self.id,
            'public_uuid':  self.public_uuid
        }

# ==============================================================================
class Colleague(Base):
    __tablename__ = 'colleagues'
    colleague1 = db.Column(db.Text(), db.ForeignKey('users.id'))
    colleague2 = db.Column(db.Text(), db.ForeignKey('users.id'))
    accepted   = db.Column(db.Boolean(), default=False)

# ==============================================================================
class Course(Base):
    __tablename__ = 'courses'
    name  = db.Column(db.Text(), nullable=False)
    users = relationship(
        'User',
        secondary='users_courses_permissions',
        secondaryjoin="and_(UserCoursePermission.users_id==User.id, User.active)",
        back_populates='courses'
    )
    sections = relationship('Section', primaryjoin="and_(Course.id==Section.courses_id, Section.active)")
    exams = relationship('Exam', primaryjoin="and_(Course.id==Exam.courses_id, Exam.active)")

    def __repr__(self):
        return '<Course %r (id=%r)>' % (self.name, self.id)

    def toJSON(self, show_users=False, show_exams=False, show_sections=False):
        course_json = {
            'name':     self.name,
            'id':       self.id,
            'permission': UserCoursePermission.query
                            .filter(UserCoursePermission.courses_id==self.id)
                            .filter(UserCoursePermission.users_id==current_user.id)
                            .one().permission.name
        }
        if show_users:
            course_json['other_users'] = [permission.toJSON() for permission in 
                            UserCoursePermission.query
                            .filter(UserCoursePermission.courses_id==self.id)
                            .filter(UserCoursePermission.users_id!=current_user.id)
                            if permission.user.active]
        if show_exams:
            course_json['exams'] = [exam.toJSON() for exam in self.exams]
        if show_sections:
            course_json['sections'] = [section.toJSON() for section in self.sections]
        return course_json

# ==============================================================================
# UserCoursePermission is a many-to-many association between users and courses
# users can have a variety of permissions for a course: they can be an:
# owner - full access to the course
# editor - can edit the course; cannot delete or share results
# readonly - can only view exam results
class CoursePermissionEnum(enum.Enum):
    own = 30
    edit = 20
    view = 10

class UserCoursePermission(Base):
    __tablename__ = 'users_courses_permissions'
    users_id    = db.Column(db.Text(), db.ForeignKey('users.id'))
    courses_id  = db.Column(db.Text(), db.ForeignKey('courses.id'))
    permission  = db.Column(db.Enum(CoursePermissionEnum), nullable=False, default=CoursePermissionEnum.own)
    user = relationship('User')
    course = relationship('Course')

    # Don't allow a user to be an owner, and 'readonly' or something
    __table_args__ = (
        db.UniqueConstraint('users_id', 'courses_id', name='unique_user_course_pair'),
    )

    def toJSON(self):
        return {
            'teachername': self.user.teachername,
            'public_uuid': self.user.public_uuid,
            'permission':  self.permission.name
        }

# ==============================================================================
class Section(Base):
    __tablename__ = 'sections'
    name = db.Column(db.Text(), nullable=False)
    courses_id = db.Column(db.Text(), db.ForeignKey('courses.id'))

    def __repr__(self):
        return '<Section %r, (id=%r)>' % (self.name, self.id)

    def toJSON(self):
        return {
            'name':        self.name,
            'id':          self.id
        }

# ==============================================================================
class Exam(Base):
    __tablename__ = 'exams'
    name = db.Column(db.Text(), nullable=False)
    courses_id = db.Column(db.Text(), db.ForeignKey('courses.id'))
    exam_format = db.Column(db.Text())
    student_exams = relationship('StudentExam', primaryjoin="and_(Exam.id==StudentExam.exams_id, StudentExam.active)")

    def __repr__(self):
        return '<Exam %r, (id=%r)>' % (self.name, self.id)

    def toJSON(self, show_student_exams=False):
        exam_json = {
            'name':        self.name,
            'id':          self.id,
            'exam_format':       self.exam_format
        }

        if show_student_exams:
            exam_json['student_exams'] = [student_exam.toJSON() for student_exam in self.student_exams]

        return exam_json

# ==============================================================================
class StudentExam(Base):
    __tablename__ = 'studentexams'
    exams_id = db.Column(db.Text(), db.ForeignKey('exams.id'))
    answers = db.Column(db.Text())

    def __repr__(self):
        return '<StudentExam (id=%r)>' % self.id
    
    def toJSON(self):
        return {
            'id': self.id,
            'answers': self.answers
        }