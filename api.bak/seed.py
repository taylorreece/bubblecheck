#!/usr/bin/env python3
# FIXME: These users are unusable.  Something something nonetype user permissions

import sys
from app import app, db
from models import User, Course, Section, UserCoursePermission
app.app_context().push()

user = User(email='a@a.com', teachername='Mr. Smith')
user.set_password('a')
friend = User(email='foo@bar.com', teachername='Mrs. Sillypants')
friend.set_password('b')
course1 = Course(name='Geometry')
course1.sections = [
    Section(name='Hour 1'),
    Section(name='Hour 2'),
    Section(name='Hour 3'),
    Section(name='Hour 4'),
]
course2 = Course(name='Algebra')
course2.sections = [
    Section(name='Hour 6'),
    Section(name='Hour 7')
]
user_course1_permission = UserCoursePermission(permission='own', user=user, course=course1)
user_course2_permission = UserCoursePermission(permission='own', user=user, course=course2)
friend_permission = UserCoursePermission(permission = 'edit', user = friend, course = course1)

db.session.add(user)
db.session.add(friend)
db.session.add(user_course1_permission)
db.session.add(user_course2_permission)
db.session.add(friend_permission)
db.session.commit()
