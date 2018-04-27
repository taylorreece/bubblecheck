#!/usr/bin/env python3
import sys
sys.path.append('..')

import base64
import json
import unittest
from app import app
from test_models import Random

rand = Random()

class CheckAPI(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(CheckAPI, self).__init__(*args, **kwargs)
        self.client = app.test_client()
    
    def test_get_marketing_pages(self):
        self.assertEqual(200, self.client.get('/').status_code)
    
    def test_user_endpoints(self):
        user = rand.user()
        user_data = {
            'teachername': user.teachername,
            'email': user.email,
            'password': 'foobarbaz'
        }
        self.assertEqual(200,
            self.client.post(
                '/api/user/add', 
                data=json.dumps(user_data),
                content_type='application/json')
            .status_code)
        response = self.client.post(
            '/api/user/token/request',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        self.assertEqual(200, response.status_code)
        token = response.data.decode()
        self.assertEqual(200, 
            self.client.get(
                '/api/user/token/check',
                headers={
                    'Authorization': 'Bearer {}'.format(token)
                }
            )
            .status_code)

if __name__ == '__main__':
    unittest.main()
