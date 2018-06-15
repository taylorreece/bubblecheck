import json 
import jwt

from flask import Blueprint
from flask import g
from flask import jsonify
from flask import render_template
from flask import request
from flask import Response
from flask import session
from flask_login import login_required
from flask_login import current_user
from bubblecheck import db
from bubblecheck.models import User

user_api_routes = Blueprint('user_api_routes', __name__)

@user_api_routes.route('/current_user', methods=['GET'])
def get_current_user():
    return jsonify(current_user.toJSON())

@user_api_routes.route('/token/request', methods=['POST'])
def token_login():
    # curl -X POST http://localhost:8080/user/token/request --data '{"email":"8LYEEX4H@IRLUH.com","password":"foobar123!"}' -H "Content-Type: application/json"
    request_data = request.get_json()
    email = request_data['email']
    password = request_data['password']
    u = db.session.query(User).filter(User.email==email).first()
    if u and u.check_password(password):
        password = u.password
        return Response(
            response=json.dumps({'jwt_token': u.create_jwt()}),
            status=200,
            mimetype='application/json')
    else:
        return ('Bad password', 401)

@user_api_routes.route('/token/check', methods=['GET'])
def token_check():
    # curl -X GET 'http://localhost:8080/user/token/check' -H "Authorization: Bearer {{TOKEN}}"
    token = request.headers.get('Authorization').replace('Bearer ', '')
    u = User().get_user_by_jwt(token)
    if u:
        return Response("Valid; Expires %s" % jwt.decode(token, verify=False)['exp'])
    else:
        return Response("Invalid", 401)

@user_api_routes.route('/token/renew', methods=['GET'])
@login_required
def token_renew():
    # curl -X GET 'http://localhost:8080/user/token/renew' -H "Authorization: Bearer {{TOKEN}}"
    return Response(
        response=json.dumps({'jwt_token': current_user.create_jwt()}),
        status=200,
        mimetype='application/json')