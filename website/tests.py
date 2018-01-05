#!/usr/bin/env python3
import random
import string
import unittest
from app import db
from app import Course
from app import Section
from app import User
from app import UserCoursePermission
from sqlalchemy.exc import IntegrityError

db.create_all()

class Random(object):
    def letters(self,N=8):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
    def email(self):
        return '{}@{}.com'.format(self.letters(8), self.letters(5))
    def user(self):
        u = User(username=self.letters(), teachername=self.letters(), email=self.email())
        u.set_password(self.letters())
        return u
    def course(self):
        return Course(name=random.choice(['Geometry','Algebra','US History','Physics','Dance','Music','Art','World History','Band','French','Japanese','German']))
    def section(self):
        return Section(name=self.letters())

rand = Random()
class BubbleCheckTestSuite(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BubbleCheckTestSuite, self).__init__(*args, **kwargs)
        self.user1 = rand.user()
        self.user1.is_admin = True
        self.user2 = rand.user()
        self.user3 = rand.user()
        self.course1 = rand.course()
        self.course2 = rand.course()
        self.course3 = rand.course()
        db.session.add_all([
            self.user1, self.user2, self.user3,
            self.course1, self.course2, self.course3
        ])
        db.session.commit()

    def test_users(self):
        self.assertIsNotNone(self.user1.id)
        self.assertTrue(self.user1.is_admin)
        self.assertFalse(self.user2.is_admin)
        self.user1.set_password('abcd1234!')
        self.assertTrue(self.user1.check_password('abcd1234!'))
        self.assertFalse(self.user1.check_password('abcd1234#'))

    def test_courses(self):
        self.assertIsNotNone(self.course1.id)

    def test_user_course_assocation(self):
        permission1 = UserCoursePermission(permission = 'owner', user = self.user1, course = self.course1)
        db.session.add(permission1)
        db.session.commit()
        self.assertTrue(self.course1 in self.user1.courses)
        self.assertFalse(self.course2 in self.user1.courses)

    def test_permissions(self):
        permission1 = UserCoursePermission(permission = 'owner', user = self.user1, course = self.course1)
        permission2 = UserCoursePermission(permission = 'editor', user = self.user1, course = self.course1)
        with self.assertRaises(IntegrityError):
            db.session.add_all([permission1, permission2])
            db.session.commit()
        db.session.rollback() # Required, as our session is now dead

    def test_sections(self):
        permission1 = UserCoursePermission(permission = 'owner', user = self.user1, course = self.course1)
        section1 = rand.section()
        section1_name = section1.name
        user1_username = self.user1.username
        section2 = rand.section()
        self.course1.sections.append(section1)
        self.course1.sections.append(section2)
        db.session.add_all([permission1, section1, section2, self.course1])
        my_user = db.session.query(User).filter_by(username=user1_username).first()
        self.assertEqual(my_user.courses[0].sections[0].name, section1_name)

if __name__ == '__main__':
    unittest.main()
