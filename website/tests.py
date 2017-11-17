#!/usr/bin/env python3
from app import db, User, Course, UserCourseAssociation, CoursePermissionEnum
db.create_all()

u = User(
    name = 'User1',
    email = 'user@test.com',
    password = 'p@ssw0rd1'
)
u.save()

c = Course(
    name = 'Geometry'
)
c.save()

a = UserCourseAssociation(permissions='readonly')
a.courses = c
u.courses.append(a)
a.save()
