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
from http import HTTPStatus

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
    
    def test_user_creation(self):
        # Create a user
        user = rand.user()
        response = self.client.post(
            '/api/user/register',
            data=json.dumps({
                'email': user.email,
                'teachername': user.teachername,
                'password': 'foobar123!',
                'repeatpassword': 'foobar123!'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # Assert you are logged in
        response = self.client.get('/api/user/current_user')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.client.get('/api/user/logout')

        # Try to create the same user again
        response = self.client.post(
            '/api/user/register',
            data=json.dumps({
                'email': user.email,
                'teachername': user.teachername,
                'password': 'foobar123!',
                'repeatpassword': 'foobar123!'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_ACCEPTABLE)

        # Assert that you get a failure if passwords don't match
        response = self.client.post(
            '/api/user/register',
            data=json.dumps({
                'email': rand.email(),
                'teachername': 'Mrs. Smith',
                'password': 'foobar123!',
                'repeatpassword': 'doesnt match'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_ACCEPTABLE)


    def test_user_login(self):
        """ Create a user via direct model invocation, then verify login works"""
        user = rand.user()
        db.session.add(user)
        db.session.commit()

        ########################################################
        # Verify bad credentials return a 401, UNAUTHORIZED
        response = self.client.post(
            '/api/user/login',
            data=json.dumps({'email': user.email, 'password': 'wrong_password'}),
            content_type='application/json')
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        ########################################################
        # The user shouldn't be able to access an endpoint protected by @login_required
        response = self.client.get('/api/user/current_user')
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        ########################################################
        # Verify good credentials return a 200
        login_response = self.client.post(
            '/api/user/login',
            data=json.dumps({'email': user.email, 'password': 'foobar123!'}),
            content_type='application/json')
        self.assertEqual(login_response.status_code, HTTPStatus.OK)

        ########################################################
        # The user should now be able to access /api/user/current_user, 
        # protected by @login_required decorator
        response = self.client.get('/api/user/current_user')
        self.assertEqual(response.status_code, HTTPStatus.OK)

        ########################################################
        # Test logout; we should now not be able to access the current_user endpoint once more
        self.client.get('/api/user/logout')
        response = self.client.get('/api/user/current_user')
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    
    def test_jwt_login(self):
        """ Create a user, create a JWT token, verify it works, and that fake tokens don't """
        user = rand.user()
        db.session.add(user)
        db.session.commit()

        token_request_json = {
            'email': user.email,
            'password': 'foobar123!'
        }

        ########################################################
        # Verify we can get a JWT token
        token_request_response = self.client.post(
            '/api/user/token/request',
            data=json.dumps(token_request_json),
            content_type='application/json')
        self.assertEqual(token_request_response.status_code, HTTPStatus.OK)
        token = json.loads(token_request_response.data.decode())['jwt_token']

        ########################################################
        # Verify we can use that token to check login
        token_check_response = self.client.get(
                '/api/user/current_user',
                headers={'Authorization': 'Bearer {}'.format(token)})
        self.assertEqual(token_check_response.status_code, HTTPStatus.OK)

        ########################################################
        # Verify we get a 302 if we try to use a bunk JWT
        bad_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IkZha2VFbWFpbEBmb29iYXIuY29tIiwiZXhwIjozMjUyNTc0NzcxMX0.GUbxfg3OWSp4yei5GTzXRNF_KF5xacNSb4mcrcr6LoI'
        bad_token_check_response = self.client.get(
            '/api/user/current_user',
            headers={'Authorization': 'Bearer {}'.format(bad_token)})
        self.assertEqual(bad_token_check_response.status_code, HTTPStatus.UNAUTHORIZED)

        ########################################################
        # Verify we can renew a JWT token
        token_renew_response = self.client.get(
                '/api/user/token/renew',
                headers={'Authorization': 'Bearer {}'.format(token)})
        self.assertEqual(token_renew_response.status_code, HTTPStatus.OK)

    def test_course_endpoints(self):
        """ Create a course, add some sections, delete some things, and rename some things """
        ########################################################
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

        ########################################################
        # Verify we can get a JWT token
        token_request_response = self.client.post(
            '/api/user/token/request',
            data=json.dumps(token_request_json),
            content_type='application/json')
        jwt_token = json.loads(token_request_response.data.decode())['jwt_token']

        ########################################################
        # Verify that we have a single course for this user
        course_list_response = self.client.get(
            '/api/course/list',
            headers={'Authorization': 'Bearer {}'.format(jwt_token)}
        )
        course_list_data = json.loads(course_list_response.data.decode())
        self.assertEqual(len(course_list_data['courses']), 1)
        self.assertEqual(course_list_data['courses'][0]['name'], 'US History')

        course_id = course_list_data['courses'][0]['id']

        ########################################################
        # Create a new course and verify that we now have two
        new_course_json = {
            'name': 'World History',
            'sections': [
                'Hour 5',
                'Hour 6',
                'Hour 7',
                'Study Hall'
            ]
        }

        course_add_response = self.client.post(
            '/api/course/add',
            headers={'Authorization': 'Bearer {}'.format(jwt_token)},
            content_type='application/json',
            data=json.dumps(new_course_json)
        )

        self.assertEqual(course_add_response.status_code, HTTPStatus.OK)
        course_add_response_json = json.loads(course_add_response.data.decode())['course']
        new_course_id = course_add_response_json['id']
        self.assertEqual(len(course_add_response_json['sections']), 4)
        self.assertEqual(course_add_response_json['sections'][1]['name'], 'Hour 6')

        course_list_response = self.client.get(
            '/api/course/list',
            headers={'Authorization': 'Bearer {}'.format(jwt_token)}
        )
        course_list_data = json.loads(course_list_response.data.decode())
        self.assertEqual(len(course_list_data['courses']), 2)

        ########################################################
        # Update the course we created
        update_course_json = {
            'name': 'Early World History'
        }

        course_update_response = self.client.post(
            '/api/course/update/{course_id}'.format(course_id=new_course_id),
            headers={'Authorization': 'Bearer {}'.format(jwt_token)},
            content_type='application/json',
            data=json.dumps(update_course_json)
        )
        self.assertEqual(course_update_response.status_code, HTTPStatus.OK)

        get_updated_course_response = self.client.get(
            '/api/course/{course_id}'.format(course_id=new_course_id),
            headers={'Authorization': 'Bearer {}'.format(jwt_token)}
        )
        get_updated_course_response_json = json.loads(get_updated_course_response.data.decode())['course']
        self.assertEqual(get_updated_course_response.status_code, 200)
        self.assertEqual(get_updated_course_response_json['name'], 'Early World History')
        self.assertEqual(len(get_updated_course_response_json['sections']), 4)

        ########################################################
        # Add a new section to our newly created course
        new_section_json = {'name': 'New Section foo'}
        add_new_section_response = self.client.post(
            '/api/course/{course_id}/section/add'.format(course_id=new_course_id),
            headers={'Authorization': 'Bearer {}'.format(jwt_token)},
            content_type='application/json',
            data=json.dumps(new_section_json)
        )
        self.assertEqual(add_new_section_response.status_code, HTTPStatus.OK)
        new_section_id = json.loads(add_new_section_response.data.decode())['section']['id']

        get_updated_course_response = self.client.get(
            '/api/course/{course_id}'.format(course_id=new_course_id),
            headers={'Authorization': 'Bearer {}'.format(jwt_token)}
        )
        get_updated_course_response_json = json.loads(get_updated_course_response.data.decode())['course']
        self.assertEqual(len(get_updated_course_response_json['sections']), 5)
        self.assertIn('New Section foo', [section['name'] for section in get_updated_course_response_json['sections']])

        ########################################################
        # Update the section we created 
        update_section_json = {'name': 'Updated section name'}
        update_section_response = self.client.post(
            '/api/course/{course_id}/section/{section_id}/update'.format(course_id=new_course_id, section_id=new_section_id),
            headers={'Authorization': 'Bearer {}'.format(jwt_token)},
            content_type='application/json',
            data=json.dumps(update_section_json)
        )
        self.assertEqual(add_new_section_response.status_code, HTTPStatus.OK)
        self.assertEqual(json.loads(update_section_response.data.decode())['section']['id'], new_section_id)
        get_updated_course_response = self.client.get(
            '/api/course/{course_id}'.format(course_id=new_course_id),
            headers={'Authorization': 'Bearer {}'.format(jwt_token)}
        )
        get_updated_course_response_json = json.loads(get_updated_course_response.data.decode())['course']
        self.assertIn('Updated section name', [section['name'] for section in get_updated_course_response_json['sections']])

        ########################################################
        # Delete the section we created
        delete_section_response = self.client.delete(
            '/api/course/{course_id}/section/{section_id}'.format(course_id=new_course_id, section_id=new_section_id),
            headers={'Authorization': 'Bearer {}'.format(jwt_token)}
        )
        self.assertEqual(delete_section_response.status_code, HTTPStatus.OK)
        get_updated_course_response = self.client.get(
            '/api/course/{course_id}'.format(course_id=new_course_id),
            headers={'Authorization': 'Bearer {}'.format(jwt_token)}
        )
        get_updated_course_response_json = json.loads(get_updated_course_response.data.decode())['course']
        self.assertEqual(len(get_updated_course_response_json['sections']), 4)
        self.assertNotIn('Updated section name', [section['name'] for section in get_updated_course_response_json['sections']])

        ########################################################
        # Delete our new course, assert we're back to one course
        delete_course_response = self.client.delete(
            '/api/course/{course_id}'.format(course_id=new_course_id),
            headers={'Authorization': 'Bearer {}'.format(jwt_token)}
        )
        self.assertEqual(delete_course_response.status_code, HTTPStatus.OK)
        course_list_response = self.client.get(
            '/api/course/list',
            headers={'Authorization': 'Bearer {}'.format(jwt_token)}
        )
        course_list_data = json.loads(course_list_response.data.decode())
        self.assertEqual(len(course_list_data['courses']), 1)
        self.assertNotIn('Early World History', [course['name'] for course in course_list_data['courses']])

if __name__ == '__main__':
    unittest.main()

# Create an exam via API

# Edit an exam via API

# Post student exam results via API

# Delete an exam via API
