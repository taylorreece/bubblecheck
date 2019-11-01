from boto3.dynamodb.conditions import Key, Attr
from flask import Blueprint
from flask import jsonify
from flask import request
from flask_login import current_user
from flask_login import login_required
from functools import wraps
from http import HTTPStatus
from shared.dynamodb import dynamodb

from uuid import uuid4

course_routes = Blueprint('course_routes', __name__)





# TODO: Add Filter expressions https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.04.html
# For active / not active








# permission is a list that might include ['own','read','write']
def course_permission_required(required_permissions):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            result = dynamodb.table.get_item(
                Key={
                    'key1': 'email_{}'.format(current_user.email),
                    'key2': 'course_{}'.format(kwargs['courseid'])
                }
            )
            if 'Item' not in result or result['Item']['permission'] not in required_permissions:
                resp = jsonify(error='Insufficient priviliges, or the course does not exist.', success=False)
                resp.status_code = HTTPStatus.UNAUTHORIZED
                return resp
            else:
                return f(*args, **kwargs)
        return decorated_function
    return decorator

@course_routes.route('/', methods=['POST'])
@login_required
def add_course():
    _course_id = str(uuid4())
    items = []
    # Add our user as an owner of the new course
    items.append({
        'Put': {
            'TableName': dynamodb.dynamo_table,
            'Item': {
                'key1': {'S': 'email_{}'.format(current_user.email)},
                'key2': {'S': 'course_{}'.format(_course_id)},
                'course_name': {'S': request.json['course_name']},
                'permission': {'S': 'own'}
            }
        }
    })
    # Add sections to the course
    for section_name in request.json['sections']:
        items.append({
            'Put': {
                'TableName': dynamodb.dynamo_table,
                'Item': {
                    'key1': {'S': 'section_{}'.format(str(uuid4()))},
                    'key2': {'S': 'course_{}'.format(_course_id)},
                    'section_name': {'S': section_name}
                }
            }
        })
    # take advantage of new dynamo transactions:
    dynamodb.client.transact_write_items(TransactItems=items)
    return jsonify(success=True, courseid=_course_id)

@course_routes.route('/my_courses', methods=['GET'])
@login_required
def my_courses():
    result = dynamodb.table.query(
        KeyConditionExpression=Key('key1').eq('email_{}'.format(current_user.email)) & Key('key2').begins_with('course_')
    )
    parsed_results = [
        {
            'name': r['course_name'],
            'permission': r['permission'],
            'id': r['key2'].replace('course_', '')
        } for r in result['Items']
    ]
    return jsonify(courses=parsed_results)

@course_routes.route('/<courseid>', methods=['GET'])
@login_required
@course_permission_required(['own','write','read'])
def get_course(courseid):
    course_results = dynamodb.table.query(
        IndexName='SecondaryGSI',
        KeyConditionExpression=Key('key2').eq('course_{}'.format(courseid))
    )
    course = {
        'users': [{
            'email': u['key1'].replace('email_', ''),
            'permission': u['permission']
        } for u in course_results['Items'] if u['key1'].startswith('email_')],
        'sections': [{
            'id': s['key1'].replace('section_', ''),
            'section_name': s['section_name']
        } for s in course_results['Items'] if s['key1'].startswith('section_')],
        'exams': [{
            'id': e['key1'].replace('exam_', ''),
            'exam_name': e['exam_name']
        } for e in course_results['Items'] if e['key1'].startswith('exam_')]
    }
    return jsonify(course=course)

# TODO: finish this function
@course_routes.route('/<courseid>', methods=['PUT'])
@login_required
@course_permission_required(['own','write'])
def update_course(courseid):
    print(request.json, flush=True)
    course_permissions = dynamodb.table.query(IndexName='SecondaryGSI',
        KeyConditionExpression=Key('key2').eq('course_{}'.format(courseid)) & Key('key1').begins_with('email_')
    )
    new_name = request.json.get('course_name')
    responses = list()
    for item in course_permissions['Items']:
        responses.append(dynamodb.table.update_item(
            Key={
                'key1': item['key1'],
                'key2': item['key2']
            },
            UpdateExpression='SET course_name = :course_name',
            ExpressionAttributeValues={
                ':course_name': new_name
            },
            ReturnValues='ALL_NEW'
        )['Attributes'])
    return jsonify(updates=responses)

# TODO: Delete exams and student exams maybe?  Or maybe turn this into a "mark active=false" or something?
@course_routes.route('/<courseid>', methods=['DELETE'])
@login_required
@course_permission_required(['own','write'])
def delete_course(courseid):
    course_items = dynamodb.table.query(IndexName='SecondaryGSI',
        KeyConditionExpression=Key('key2').eq('course_{}'.format(courseid))
    )['Items'] + dynamodb.table.query(
        KeyConditionExpression=Key('key1').eq('course_{}'.format(courseid))
    )['Items']
    for item in course_items:
        dynamodb.table.delete_item(
            Key={
                'key1': item['key1'],
                'key2': item['key2']
            },
        )
    return jsonify(deleted=course_items, success=True)