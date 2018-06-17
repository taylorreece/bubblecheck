#!/usr/bin/env python3
import json
import random
import string
import sys
import unittest
sys.path.append('..')
from bubblecheck.models import User, Course, Section
from bubblecheck import app
from bubblecheck import db


class Random(object):
    def letters(self,N=8):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
    def email(self):
        return '{}@{}.com'.format(self.letters(8), self.letters(5))
    def user(self):
        u = User(teachername=self.letters(), email=self.email())
        u.set_password('foobar123!')
        return u
    def course(self):
        return Course(name=random.choice(['Geometry','Algebra','US History','Physics','Dance','Music','Art','World History','Band','French','Japanese','German']))
    def section(self):
        return Section(name=self.letters())

rand = Random()

class CheckAPI(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(CheckAPI, self).__init__(*args, **kwargs)
        self.client = app.test_client()

    def test_user_login(self):
        """ Create a user via direct model invocation, then verify login works"""
        user = rand.user()
        db.session.add(user)
        db.session.commit()

        # Verify bad credentials return a 401
        response = self.client.post(
            '/user/login',
            data=dict(email=user.email, password='wrong_password'),
            follow_redirects=True)
        self.assertEqual(response.status_code, 401)

        # The user shouldn't be able to access an endpoint protected by @login_required
        # They should instead be redirected, so get a 302 return code
        response = self.client.get('/user/testlogin')
        self.assertEqual(response.status_code, 302)

        # Verify good credentials return a 200
        login_response = self.client.post(
            '/user/login',
            data=dict(email=user.email, password='foobar123!'),
            follow_redirects=True)
        self.assertEqual(login_response.status_code, 200)

        # The user should now be able to access /user/testlogin, protected by @login_required decorator
        response = self.client.get('/user/testlogin')
        self.assertEqual(response.status_code, 200)

        # Test logout; we should now not be able to access the testlogin endpoint once more
        self.client.get('/user/logout')
        response = self.client.get('/user/testlogin')
        self.assertEqual(response.status_code, 302)
    
    def test_jwt_login(self):
        """ Create a user, create a JWT token, verify it works, and that fake tokens don't """
        user = rand.user()
        db.session.add(user)
        db.session.commit()

        token_request_json = {
            'email': user.email,
            'password': 'foobar123!'
        }

        # Verify we can get a JWT token
        token_request_response = self.client.post(
            '/api/user/token/request',
            data=json.dumps(token_request_json),
            content_type='application/json')
        self.assertEqual(token_request_response.status_code, 200)
        token = json.loads(token_request_response.data.decode())['jwt_token']

        # Verify we can use that token to check login
        token_check_response = self.client.get(
                '/user/testlogin',
                headers={'Authorization': 'Bearer {}'.format(token)})
        self.assertEqual(token_check_response.status_code, 200)

        # Verify we get a 302 if we try to use a bunk JWT
        bad_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IkZha2VFbWFpbEBmb29iYXIuY29tIiwiZXhwIjozMjUyNTc0NzcxMX0.GUbxfg3OWSp4yei5GTzXRNF_KF5xacNSb4mcrcr6LoI'
        bad_token_check_response = self.client.get(
            '/user/testlogin',
            headers={'Authorization': 'Bearer {}'.format(bad_token)})
        self.assertEqual(bad_token_check_response.status_code, 302)

        # Verify we can renew a JWT token
        token_renew_response = self.client.get(
                '/api/user/token/renew',
                headers={'Authorization': 'Bearer {}'.format(token)})
        self.assertEqual(token_renew_response.status_code, 200)

    def test_course_endpoints(self):
        # Set up a user and a course
        user = rand.user()
        user.set_password('foobar123!')
        course = Course(name='US History')
        section1 = Section(name='Hour 1')
        section2 = Section(name='Hour 2')
        course.sections = [section1, section2]
        user.courses.append(course)
        db.session.add_all([user, course, section1, section2])
        db.session.commit()

        token_request_json = {
            'email': user.email,
            'password': 'foobar123!'
        }

        # Verify we can get a JWT token
        token_request_response = self.client.post(
            '/api/user/token/request',
            data=json.dumps(token_request_json),
            content_type='application/json')
        jwt_token = json.loads(token_request_response.data.decode())['jwt_token']

        # Verify that we have a single course for this user
        course_list_response = self.client.get(
            '/api/course/list',
            headers={'Authorization': 'Bearer {}'.format(jwt_token)}
        )
        course_list_data = json.loads(course_list_response.data.decode())
        self.assertEqual(len(course_list_data['courses']), 1)
        self.assertEqual(course_list_data['courses'][0]['name'], 'US History')

        course_id = course_list_data['courses'][0]['id']

        # TODO: pull down data on specific course, add a section, etc.
        
if __name__ == '__main__':
    unittest.main()

# Create course using JWT token

# Create a course and sections via API using cookies

# Edit the course name via API

# Add a section via API
# Verify number of sections

# Delete a section via API
# Verify new number of sections

# Delete the course via API

# Create an exam via API

# Edit an exam via API

# Post student exam results via API

# Delete an exam via API
