#!/usr/bin/env python3
from app import db, User, Course, UserCoursePermission, CoursePermissionEnum
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

permission = UserCoursePermission(permission='readonly')
permission.course = c
permission.user = u
permission.save()