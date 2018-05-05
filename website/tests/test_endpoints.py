#!/usr/bin/env python3
import sys
sys.path.append('..')

import base64
import json
import time
import unittest
from app import app
from app import db
from app.models import Course
from app.models import Section
from app.models import User
from app.models import UserCoursePermission
from test_models import Random

rand = Random()

class CheckAPI(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(CheckAPI, self).__init__(*args, **kwargs)
        self.client = app.test_client()
    
    def test_get_marketing_pages(self):
        self.assertEqual(200, self.client.get('/').status_code)
    
    def test_course_endpoints(self):
        user = rand.user()
        course1 = rand.course()
        course2 = rand.course()
        permission1 = UserCoursePermission(permission = 'owner', user = user, course = course1)
        permission2 = UserCoursePermission(permission = 'owner', user = user, course = course2)
        db.session.add_all([user, course1, course2, permission1, permission2])
        db.session.commit()
        db.session.refresh(course1)
        self.client.post(
            '/user/login',
            data=dict(email=user.email, password='foobar123!'), 
            follow_redirects=True)
        course_list_response = self.client.get('/api/course/list')
        courses = json.loads(course_list_response.data.decode())
        self.assertEqual(course_list_response.status_code, 200)
        self.assertEqual(len(courses), 2)
        self.assertIn(course1.id, [x['id'] for x in courses])

    def test_user_endpoints(self):
        user = rand.user()
        user_data = user.serialize()
        user_data.update({'password': 'foobar123!'})
        self.assertEqual(200,
            self.client.post(
                '/api/user/add', 
                data=json.dumps(user_data),
                content_type='application/json'
            ).status_code)
        response = self.client.post(
            '/api/user/token/request',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        self.assertEqual(200, response.status_code)
        token = json.loads(response.data.decode())['jwt_token']
        response = self.client.get(
                '/api/user/token/check',
                headers={
                    'Authorization': 'Bearer {}'.format(token)
                })
        self.assertEqual(200, response.status_code)
        time.sleep(2)
        response = self.client.get(
                '/api/user/token/renew',
                headers={
                    'Authorization': 'Bearer {}'.format(token)
                }
            )
        self.assertEqual(200, response.status_code)
        # Assert logins work
        self.assertEqual(200,
            self.client.post(
                '/user/login',
                data=dict(
                    email=user_data['email'],
                    password=user_data['password']
                ), 
                follow_redirects=True
            ).status_code)
        self.assertEqual(401,
            self.client.post(
                '/user/login',
                data=dict(
                    email=user_data['email'],
                    password='incorrect_password'
                ),
                follow_redirects=True
            ).status_code)

if __name__ == '__main__':
    unittest.main()
