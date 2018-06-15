#!/usr/bin/env python3
import sys
sys.path.append('..')

from bubblecheck import db
from bubblecheck.models import User, Course, Section, UserCoursePermission

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
user.courses = [course1, course2]
friend_permission = UserCoursePermission(permission = 'editor', user = friend, course = course1)

db.session.add(user)
db.session.add(friend)
db.session.add(friend_permission)
db.session.commit()