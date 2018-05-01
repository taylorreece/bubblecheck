from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from app import db
import datetime
import enum
import jwt

# ==============================================================================
# Define a base model for other database tables to inherit
class Base(db.Model):
    __abstract__  = True
    id = db.Column(db.Integer, primary_key=True)
    created  = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.current_timestamp())
    modified = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    active   = db.Column(db.Boolean(), nullable=False, default=True)

    sensitive_columns = []

    def serialize(self, show_sensitive_columns=False):
        """Return object data in easily serializeable format"""
        return { 
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name not in self.sensitive_columns 
                or show_sensitive_columns
        }

# ==============================================================================
class User(UserMixin, Base):
    __tablename__ = 'users'
    sensitive_columns = ['password']
    email = db.Column(db.Text(), nullable=False, unique=True)
    teachername = db.Column(db.Text(), nullable=False)
    password = db.Column(db.Text(), nullable=False)
    is_admin = db.Column(db.Boolean(), nullable=False, default=False)
    courses = relationship(
        "Course",
        secondary='users_courses_permissions',
        back_populates="users"
    )
    logged_in = False
    
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

# ==============================================================================
class Course(Base):
    __tablename__ = 'courses'
    name    = db.Column(db.Text(), nullable=False)
    users = relationship(
        "User",
        secondary='users_courses_permissions',
        back_populates="courses"
    )
    sections = relationship("Section")
    exams = relationship("Exam")

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<Course %r (id=%r)>' % (self.name, self.id)

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
    permission  = db.Column(db.Enum(CoursePermissionEnum), nullable=False)
    user = relationship("User")
    course = relationship("Course")

    # Don't allow a user to be an owner, and 'readonly' or something
    __table_args__ = (
        db.UniqueConstraint('users_id', 'courses_id', name='unique_user_course_pair'),
    )

# ==============================================================================
class Section(Base):
    __tablename__ = 'sections'
    name = db.Column(db.Text(), nullable=False)
    courses_id = db.Column(db.Integer, db.ForeignKey('courses.id'))

    def __repr__(self):
        return '<Section %r, (id=%r)>' % (self.name, self.id)

# ==============================================================================
class Exam(Base):
    __tablename__ = 'exams'
    name = db.Column(db.Text(), nullable=False)
    courses_id = db.Column(db.Integer, db.ForeignKey('courses.id'))

    def __repr__(self):
        return '<Exam %r, (id=%r)>' % (self.name, self.id)
