from sqlalchemy.orm import relationship
from app import db
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

if db.engine.name == 'postgresql':
    from app.sqlalchemy_extensions.uuid_column import UUID
    id_column_type = UUID
    id_column_server_default = db.text("uuid_in(md5(random()::text || now()::text)::cstring)")
else:
    id_column_type = db.Integer
    id_column_server_default = None

# ==============================================================================
# Define a base model for other database tables to inherit
# We'll use UUIDs in postgresql, but just ids for testing
class Base(db.Model):
    __abstract__  = True
    id = db.Column(id_column_type, primary_key=True, server_default=id_column_server_default)
    created  = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.current_timestamp())
    modified = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def save(self):
        db.session.add(self)
        db.session.commit()

# ==============================================================================
class User(Base):
    __tablename__ = 'users'
    name     = db.Column(db.Text(), nullable=False)
    email    = db.Column(db.Text(), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)
    is_admin = db.Column(db.Boolean(), nullable=False, default=False)
    courses = relationship(
        "Course",
        secondary='users_courses_permissions',
        back_populates="users"
    )

    def __repr__(self):
        return '<User %r>' % (self.name)

# ==============================================================================
class Course(Base):
    __tablename__ = 'courses'
    name    = db.Column(db.Text(), nullable=False)
    users = relationship(
        "User",
        secondary='users_courses_permissions',
        back_populates="courses"
    )

    def __repr__(self):
        return '<Course %r>' % (self.name)

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
    users_id    = db.Column(id_column_type, db.ForeignKey('users.id'))
    courses_id  = db.Column(id_column_type, db.ForeignKey('courses.id'))
    permission = db.Column(db.Enum(CoursePermissionEnum), nullable=False)
    user = relationship("User")
    course = relationship("Course")
