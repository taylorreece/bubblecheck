#!/usr/bin/env python3
import sys
sys.path.append('..')

import unittest
from app import app

class CheckAPI(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(CheckAPI, self).__init__(*args, **kwargs)
        self.client = app.test_client()

    def test_get_marketing_pages(self):
        self.assertEqual(200, self.client.get('/').status_code)

if __name__ == '__main__':
    unittest.main()
