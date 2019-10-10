#!/usr/bin/env python3
import json
import os
import random
import string
import sys
import unittest
sys.path.append(os.path.join('..','api'))
from app import app, db
from models import User, Course, Section, Exam, StudentExam
from http import HTTPStatus

app.app_context().push() # Get proper database context

class Random(object):
    def letters(self,N=8):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(N))
    def email(self):
        return '{}@{}.com'.format(self.letters(8), self.letters(5))
    def user(self):
        u = User(teachername=self.letters(), email=self.email())
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

    def test_course_endpoints(self):
        """ Create a course, add some sections, delete some things, and rename some things """
        ########################################################
        # Set up a user and a course
        user = rand.user()
        course = Course(name='US History')
        section1 = Section(name='Hour 1')
        section2 = Section(name='Hour 2')
        course.sections = [section1, section2]
        user.courses.append(course)
        db.session.add_all([user, course, section1, section2])
        db.session.commit()

        token_request_json = {
            'email': user.email
        }

        ########################################################
        # Verify that we have a single course for this user
        course_list_response = self.client.get(
            '/api/course/',
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
            '/api/course/',
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
            '/api/course/',
            headers={'Authorization': 'Bearer {}'.format(jwt_token)}
        )
        course_list_data = json.loads(course_list_response.data.decode())
        self.assertEqual(len(course_list_data['courses']), 1)
        self.assertNotIn('Early World History', [course['name'] for course in course_list_data['courses']])

    def test_exam_endpoints(self):
        user = rand.user()
        course = Course(name='World Lit')
        section1 = Section(name='Hour 1')
        section2 = Section(name='Hour 2')
        course.sections = [section1, section2]
        exam1 = Exam(name='Exam 1', exam_format='DDD..EEDD')
        exam2 = Exam(name='Exam 2', exam_format='..FFFFFFFFFFFF')
        course.exams = [exam1, exam2]
        user.courses.append(course)
        db.session.add(course)
        db.session.add_all([user, section1, section2, exam1, exam2])
        db.session.commit()
        db.session.refresh(course)
        db.session.refresh(exam1)

        ##############################################
        # Verify that we have two exams in this course
        exams_list_response = self.client.get(
            '/api/course/{course_id}/exams'.format(course_id=course.id),
            headers={'Authorization': 'Bearer {}'.format(jwt_token)}
        )
        self.assertEqual(exams_list_response.status_code, HTTPStatus.OK)
        exam_list_data = json.loads(exams_list_response.data.decode())
        self.assertEqual(len(exam_list_data['exams']), 2)

        ###############################################
        # Verify that a specific exam has the correct name and format
        self.assertIn('Exam 1', [exam['name'] for exam in exam_list_data['exams']])
        self.assertNotIn('Exam Foo', [exam['name'] for exam in exam_list_data['exams']])
        self.assertIn('DDD..EEDD', [exam['exam_format'] for exam in exam_list_data['exams']])
        
        ###############################################
        # Add an Exam
        new_exam = Exam(name='Exam 3', exam_format='DDDDD')
        new_exam_request_response = self.client.post(
            '/api/course/{course_id}/exam/add'.format(course_id=course.id),
            data=json.dumps(new_exam.toJSON()),
            content_type='application/json',
            headers={'Authorization': 'Bearer {}'.format(jwt_token)}
        )
        self.assertEqual(new_exam_request_response.status_code, HTTPStatus.OK)
        exams_list_response = self.client.get(
            '/api/course/{course_id}/exams'.format(course_id=course.id),
            headers={'Authorization': 'Bearer {}'.format(jwt_token)}
        )
        exam_list_data = json.loads(exams_list_response.data.decode())
        # we now have 3 exams
        self.assertEqual(len(exam_list_data['exams']), 3)
        new_exam_id = json.loads(new_exam_request_response.data.decode())['exam']['id']

        ###############################################
        # Edit an exam
        update_exam_response = self.client.post(
            '/api/course/{course_id}/exam/{exam_id}/update'.format(course_id=course.id, exam_id=new_exam_id),
            data=json.dumps({'name': 'Exam 4', 'exam_format': 'CCC'}),
            content_type='application/json',
            headers={'Authorization': 'Bearer {}'.format(jwt_token)}
        )
        self.assertEqual(update_exam_response.status_code, HTTPStatus.OK)
        update_exam_response_data = json.loads(update_exam_response.data.decode())
        self.assertEqual('CCC', update_exam_response_data['exam']['exam_format'])
        self.assertEqual('Exam 4', update_exam_response_data['exam']['name'])

        ###############################################
        # Delete an Exam
        delete_exam_response = self.client.delete(
            '/api/course/{course_id}/exam/{exam_id}'.format(course_id=course.id, exam_id=new_exam_id),
            headers={'Authorization': 'Bearer {}'.format(jwt_token)}
        )
        exams_list_response = self.client.get(
            '/api/course/{course_id}/exams'.format(course_id=course.id),
            headers={'Authorization': 'Bearer {}'.format(jwt_token)}
        )
        exam_list_data = json.loads(exams_list_response.data.decode())
        # we should be back to two exams
        self.assertEqual(len(exam_list_data['exams']), 2)

        ###############################################
        ###############################################
        # Create three student exams
        for answers in ['DDDTTEEDD', 'ABCTFDEAC', 'DCBFFEAAA']:
            create_student_exam_response = self.client.post(
                '/api/course/{course_id}/exam/{exam_id}/student_exam'.format(course_id=course.id, exam_id=exam1.id),
                data=json.dumps({'answers': answers}),
                content_type='application/json',
                headers={'Authorization': 'Bearer {}'.format(jwt_token)})
        exam1 = Exam.query.get(exam1.id) # 'db.session.refresh' doesn't work here, as we're on to a different db session
        self.assertEqual(len(exam1.student_exams), 3)
        exam_response = self.client.get(
            '/api/course/{course_id}/exam/{exam_id}'.format(course_id=course.id, exam_id=exam1.id),
            headers={'Authorization': 'Bearer {}'.format(jwt_token)})
        exam_response_data = json.loads(exam_response.data.decode())
        self.assertEqual(len(exam_response_data['exam']['student_exams']), 3)

        ###############################################
        # Update one of those student exams
        student_exam_id = exam_response_data['exam']['student_exams'][0]['id']
        self.client.post(
            '/api/course/{course_id}/exam/{exam_id}/student_exam/{student_exam_id}'.format(
                course_id = course.id,
                exam_id = exam1.id,
                student_exam_id = student_exam_id
            ),
            data=json.dumps({'answers': 'AAAFFAAAA'}),
            content_type='application/json',
            headers={'Authorization': 'Bearer {}'.format(jwt_token)})
        student_exam = StudentExam.query.get(student_exam_id)
        self.assertEqual(student_exam.answers, 'AAAFFAAAA')

        ###############################################
        # Delete a student exam
        delete_student_exam_response = self.client.delete(
            '/api/course/{course_id}/exam/{exam_id}/student_exam/{student_exam_id}'.format(
                course_id = course.id,
                exam_id = exam1.id,
                student_exam_id = student_exam_id
            ),
            content_type='application/json',
            headers={'Authorization': 'Bearer {}'.format(jwt_token)})
        exam1 = Exam.query.get(exam1.id)
        self.assertEqual(len(exam1.student_exams), 2)
        


if __name__ == '__main__':
    unittest.main()
