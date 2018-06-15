from flask_login import UserMixin
from flask_login import current_user
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from bubblecheck import db
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
    id = db.Column(db.Integer, primary_key=True)
    created  = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.current_timestamp())
    modified = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    active   = db.Column(db.Boolean(), nullable=False, default=True)

# ==============================================================================
class User(UserMixin, Base):
    __tablename__ = 'users'
    email = db.Column(db.Text(), nullable=False, unique=True)
    teachername = db.Column(db.Text(), nullable=False)
    password = db.Column(db.Text(), nullable=False)
    is_admin = db.Column(db.Boolean(), nullable=False, default=False)
    public_uuid = db.Column(db.Text(), nullable=False, default=generate_uuid, unique=True)
    courses = relationship(
        'Course',
        secondary='users_courses_permissions',
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

    def get_user_by_jwt(self, token):
        try:
            decoded_token = jwt.decode(token, verify=False)
            u = db.session.query(User).filter(User.email==decoded_token['email']).first()
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
class Course(Base):
    __tablename__ = 'courses'
    name    = db.Column(db.Text(), nullable=False)
    users = relationship(
        'User',
        secondary='users_courses_permissions',
        back_populates='courses'
    )
    sections = relationship('Section')
    exams = relationship('Exam')

    def __repr__(self):
        return '<Course %r (id=%r)>' % (self.name, self.id)

    def toJSON(self):
        return {
            'name':        self.name,
            'id':          self.id,
            'sections':    [section.toJSON() for section in self.sections],
            'exams':       [exam.toJSON() for exam in self.exams],
            'other_users': [permission.toJSON() for permission in 
                            db.session.query(UserCoursePermission)
                            .filter(UserCoursePermission.courses_id==self.id)
                            .filter(UserCoursePermission.users_id!=current_user.id)
                            ],
            'permission':  db.session.query(UserCoursePermission)
                            .filter(UserCoursePermission.courses_id==self.id)
                            .filter(UserCoursePermission.users_id==current_user.id)
                            .first().permission.name
        }

# ==============================================================================
# UserCoursePermission is a many-to-many association between users and courses
# users can have a variety of permissions for a course: they can be an:
# owner - full access to the course
# editor - can edit the course; cannot delete or share results
# readonly - can only view exam results
class CoursePermissionEnum(enum.Enum):
    owner = 1
    editor = 2
    readonly = 3

class UserCoursePermission(Base):
    __tablename__ = 'users_courses_permissions'
    users_id    = db.Column(db.Integer, db.ForeignKey('users.id'))
    courses_id  = db.Column(db.Integer, db.ForeignKey('courses.id'))
    permission  = db.Column(db.Enum(CoursePermissionEnum), nullable=False, default=CoursePermissionEnum.owner)
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
    courses_id = db.Column(db.Integer, db.ForeignKey('courses.id'))

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
    courses_id = db.Column(db.Integer, db.ForeignKey('courses.id'))

    def __repr__(self):
        return '<Exam %r, (id=%r)>' % (self.name, self.id)

    def toJSON(self):
        return {
            'name':        self.name,
            'id':          self.id
        }