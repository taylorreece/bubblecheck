import datetime
import jwt

from boto3.dynamodb.conditions import Key, Attr
from flask_login import UserMixin
from shared.bcjwt import bcjwt_secret
from shared.dynamodb import dynamodb
JWT_ALGORITHM='HS256'

# We use 'email' as the 'id' of a user for convienence sake; id is not used currently.

class User(UserMixin):
    def __init__(self, email=None):
        self.id = None
        self.exists = False
        self.teacher_name = '-'
        self.email = None
        self.is_admin = False
        self.active = True
        if not email:
            return
        result = dynamodb.table.query(
            KeyConditionExpression=Key('key1').eq('email_{}'.format(email)) & Key('key2').begins_with('user_')
        )
        if result['Count'] != 1: # There should only be one user for each email
            return
        self.email = result['Items'][0]['key1'].replace('email_', '')
        self.id = result['Items'][0]['key2'].replace('user_', '')
        self.teacher_name = result['Items'][0]['teacher_name']
        self.is_admin = result['Items'][0]['is_admin']
        self.active = result['Items'][0]['active']
        self.exists = True

    def get_id(self):
        return self.email

    def save(self):
        item = {
                'key1': 'email_{}'.format(self.email),
                'key2': 'user_{}'.format(self.id),
                'is_admin': self.is_admin,
                'active': self.active,
                'teacher_name': self.teacher_name
        }
        self.exists = True
        dynamodb.table.put_item(Item=item)

    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'teacher_name': self.teacher_name,
            'is_admin': self.is_admin,
            'active': self.active
        }
        
    def __str__(self):
        return str(self.to_json())

    def create_jwt(self):
        return jwt.encode(
            payload={
                'email': self.email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24*30)
            },
            key=bcjwt_secret.get_secret(),
            algorithm=JWT_ALGORITHM
        ).decode()

    def get_user_by_jwt(token):
        try:
            decoded_token = jwt.decode(token, verify=False)
            email = decoded_token['email']
            if jwt.decode(token, bcjwt_secret.get_secret(), algorithms=[JWT_ALGORITHM]):
                return User(email)
            else:
                return None
        except jwt.exceptions.DecodeError as e:
            return None
