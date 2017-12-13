#!/usr/bin/env python3
import random
import string
import unittest
from app import db, User, Course, UserCoursePermission
from sqlalchemy.exc import IntegrityError

db.create_all()

class Random(object):
    def letters(self,N=8):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
    def email(self):
        return '{}@{}.com'.format(self.letters(8), self.letters(5))
    def user(self):
        return User(name=self.letters(), email=self.email(), password=self.letters())
    def course(self):
        return Course(name=self.letters())

rand = Random()
class BubbleCheckTestSuite(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BubbleCheckTestSuite, self).__init__(*args, **kwargs)
        self.user1 = rand.user(); self.user1.is_admin = True; self.user1.save()
        self.user2 = rand.user(); self.user2.save()
        self.user3 = rand.user(); self.user3.save()
        self.course1 = rand.course(); self.course1.save()
        self.course2 = rand.course(); self.course2.save()
        self.course3 = rand.course(); self.course3.save()

    def test_users(self):
        self.assertIsNotNone(self.user1.id)
        self.assertTrue(self.user1.is_admin)
        self.assertFalse(self.user2.is_admin)

    def test_courses(self):
        self.assertIsNotNone(self.course1.id)

    def test_user_course_assocation(self):
        permission1 = UserCoursePermission(permission = 'owner', user = self.user1, course = self.course1)
        permission1.save()
        self.assertTrue(self.course1 in self.user1.courses)
        self.assertFalse(self.course2 in self.user1.courses)

    def test_permissions(self):
        permission1 = UserCoursePermission(permission = 'owner', user = self.user1, course = self.course1)
        permission1.save()
        permission2 = UserCoursePermission(permission = 'editor', user = self.user1, course = self.course1)
        with self.assertRaises(IntegrityError):
            permission2.save()
        db.session.rollback() # Required, as our session is now dead

if __name__ == '__main__':
    unittest.main()