import json 
import jwt
import requests

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
from flask import url_for
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from http import HTTPStatus

from database import db
from models import User
from cognito import cognito

user_api_routes = Blueprint('user_api_routes', __name__)

@user_api_routes.route('/current_user', methods=['GET'])
@login_required
def get_current_user():
    return jsonify(user=current_user.toJSON(), success=True)

@user_api_routes.route('/oauth/cognito/callback', methods=['GET'])
def login_via_cognito_callback():
    login_code = request.args.get('code')
    email = cognito.get_email_from_code(
        code=login_code, 
        callback_url=url_for(
            'user_api_routes.login_via_cognito_callback',
            _external=True
    ))
    user = User.query.filter(User.email==email).one_or_none()
    if user:
        login_user(user)
        return redirect('/api/user/current_user')
    else:
        _user = User(email=email)
        db.session.add(_user)
        db.session.commit()
        db.session.refresh(_user)
        login_user(_user)
        return redirect('/api/user/current_user')

@user_api_routes.route('/oauth/cognito/login', methods=['GET'])
def oauth_login_redirect():
    redirect_url=cognito.cognito_login_url(
        callback_url=url_for(
            'user_api_routes.login_via_cognito_callback',
            _external=True
    ))
    return redirect(redirect_url)

# @user_api_routes.route('/login', methods=['POST'])
# def user_login_view():
#     request_data = request.get_json()
#     email = request_data['email']
#     password = request_data['password']
#     u = User.query.filter(User.email==email).one_or_none()
#     if u and u.check_password(password):
#         login_user(u)
#         return jsonify(user=u.toJSON(), success=True)
#     resp = jsonify(error='Login Incorrect', success=False)
#     resp.status_code = HTTPStatus.UNAUTHORIZED
#     return resp

@user_api_routes.route('/logout', methods=['GET'])
def user_logout_view():
    logout_user()
    return jsonify(success=True)

# @user_api_routes.route('/register', methods=['POST'])
# def user_register():
#     request_data = request.get_json()
#     email = request_data['email']
#     password = request_data['password']
#     repeatpassword = request_data['repeatpassword']
#     teachername = request_data['teachername']
#     u = User.query.filter(User.email==email).one_or_none()
#     if u:
#         ret = jsonify(error='A user with that email already exists.', success=False)
#         ret.status_code = HTTPStatus.NOT_ACCEPTABLE
#         return ret
#     if password != repeatpassword:
#         ret = jsonify(error='Your passwords do not match', success=False)
#         ret.status_code = HTTPStatus.NOT_ACCEPTABLE
#         return ret
#     _user = User(
#         email=email,
#         teachername=teachername
#     )
#     _user.set_password(password)
#     db.session.add(_user)
#     db.session.commit()
#     db.session.refresh(_user)
#     login_user(_user)
#     return jsonify(user=_user.toJSON(), success=True)

@user_api_routes.route('/token/request', methods=['POST'])
def token_login():
    # curl -X POST http://localhost:8080/user/token/request --data '{"email":"8LYEEX4H@IRLUH.com","password":"foobar123!"}' -H "Content-Type: application/json"
    request_data = request.get_json()
    email = request_data['email']
    password = request_data['password']
    u = User.query.filter(User.email==email).one_or_none()
    if u and u.check_password(password):
        password = u.password
        return jsonify(jwt_token=u.create_jwt(), success=True)
    else:
        resp = jsonify(error='No such user found', success=False)
        resp.status_code = HTTPStatus.NOT_FOUND
        return resp

@user_api_routes.route('/token/check', methods=['GET'])
def token_check():
    # curl -X GET 'http://localhost:8080/user/token/check' -H "Authorization: Bearer {{TOKEN}}"
    token = request.headers.get('Authorization').replace('Bearer ', '')
    u = User.get_user_by_jwt(token)
    if u:
        return jsonify(expires=jwt.decode(token, verify=False)['exp'], success=True)
    else:
        resp = jsonify(error="Invalid JWT token", success=False)
        resp.status_code = HTTPStatus.UNAUTHORIZED
        return resp

@user_api_routes.route('/token/renew', methods=['GET'])
@login_required
def token_renew():
    # curl -X GET 'http://localhost:8080/user/token/renew' -H "Authorization: Bearer {{TOKEN}}"
    return jsonify(jwt_token=current_user.create_jwt(), success=True)

@user_api_routes.route('/flash_messages', methods=['GET'])
def get_flash_messages():
    messages = [{
            'message': message,
            'category': category
        } for category, message in get_flashed_messages(with_categories=True)]
    return jsonify(messages=messages, success=True)