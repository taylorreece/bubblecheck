import json 
import jwt

from flask import Blueprint
from flask import flash
from flask import g
from flask import get_flashed_messages
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import Response
from flask import session
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from http import HTTPStatus
from bubblecheck import db
from bubblecheck.models import User

user_api_routes = Blueprint('user_api_routes', __name__)

@user_api_routes.route('/current_user', methods=['GET'])
@login_required
def get_current_user():
    return jsonify(current_user.toJSON())

@user_api_routes.route('/login', methods=['POST'])
def user_login_view():
    request_data = request.get_json()
    email = request_data['email']
    password = request_data['password']
    u = User.query.filter(User.email==email).one_or_none()
    if u and u.check_password(password):
        login_user(u)
        return 'Success', 200
    return 'Login Incorrect', 401

@user_api_routes.route('/logout', methods=['GET'])
def user_logout_view():
    logout_user()
    return redirect('/')

@user_api_routes.route('/register', methods=['POST'])
def user_register():
    request_data = request.get_json()
    email = request_data['email']
    password = request_data['password']
    repeatpassword = request_data['repeatpassword']
    teachername = request_data['teachername']
    u = User.query.filter(User.email==email).one_or_none()
    if u:
        ret = jsonify(error='A user with that email already exists.')
        ret.status_code = HTTPStatus.NOT_ACCEPTABLE
        return ret
    if password != repeatpassword:
        ret = jsonify(error='Your passwords do not match')
        ret.status_code = HTTPStatus.NOT_ACCEPTABLE
        return ret
    _user = User(
        email=email,
        teachername=teachername
    )
    _user.set_password(password)
    db.session.add(_user)
    db.session.commit()
    db.session.refresh(_user)
    login_user(_user)
    return 'Success', 200

@user_api_routes.route('/token/request', methods=['POST'])
def token_login():
    # curl -X POST http://localhost:8080/user/token/request --data '{"email":"8LYEEX4H@IRLUH.com","password":"foobar123!"}' -H "Content-Type: application/json"
    request_data = request.get_json()
    email = request_data['email']
    password = request_data['password']
    u = User.query.filter(User.email==email).one_or_none()
    if u and u.check_password(password):
        password = u.password
        return jsonify(jwt_token=u.create_jwt())
    else:
        resp = jsonify(error='No such user found')
        resp.status_code = HTTPStatus.NOT_FOUND
        return resp

@user_api_routes.route('/token/check', methods=['GET'])
def token_check():
    # curl -X GET 'http://localhost:8080/user/token/check' -H "Authorization: Bearer {{TOKEN}}"
    token = request.headers.get('Authorization').replace('Bearer ', '')
    u = User.get_user_by_jwt(token)
    if u:
        return jsonify(expires=jwt.decode(token, verify=False)['exp'])
    else:
        return Response("Invalid", 401)

@user_api_routes.route('/token/renew', methods=['GET'])
@login_required
def token_renew():
    # curl -X GET 'http://localhost:8080/user/token/renew' -H "Authorization: Bearer {{TOKEN}}"
    return jsonify(jwt_token=current_user.create_jwt())

@user_api_routes.route('/flash_messages', methods=['GET'])
def get_flash_messages():
    messages = [{
            'message': message,
            'category': category
        } for category, message in get_flashed_messages(with_categories=True)]
    return jsonify(messages=messages)