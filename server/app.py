#!/usr/bin/env python

import boto3
import os
import uuid

from flask import Flask, g, request, session, jsonify

app = Flask(__name__)

LOCAL_DEVELOPMENT = os.environ.get('LOCAL_DEVELOPMENT', default=False)

if LOCAL_DEVELOPMENT:
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
else:
    dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table(os.environ.get('DYNAMODB_TABLE'))

@app.route('/')
def home():
    response = table.put_item(
        Item={
            'pk': str(uuid.uuid4()),
            'sk': 'user',
            'age': 25,
            'foo': 'bar'
        }
    )
    return response

app.run(host='0.0.0.0', port=5000, debug=True)