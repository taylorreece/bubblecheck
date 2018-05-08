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
from app import db
from app.models import User

user_api_routes = Blueprint('user_api_routes', __name__)

@user_api_routes.route('/add', methods=['POST'])
def add():
    # TODO 
    #  update request to allow for form-data or json
    #  validate data against wtforms
    #  note to self: cast get_json() data to MultiDict() from werkzeug to validate json-supplied data
    request_data = request.get_json()
    new_user = User(
        teachername = request_data['teachername'],
        email = request_data['email'],
        is_admin = False
    )
    new_user.set_password(request_data['password'])
    db.session.add(new_user)
    db.session.commit()
    return Response(status=200)

@user_api_routes.route('/token/request', methods=['POST'])
def token_login():
    # curl -X POST http://localhost:8080/api/user/token/request --data '{"email":"8LYEEX4H@IRLUH.com","password":"foobar123!"}' -H "Content-Type: application/json"
    # or 
    #  curl -X POST http://localhost:8080/api/user/token/request -F 'email=WOFP1DVL@M0WU2.com' -F 'password=foobar123!'
    if request.mimetype == 'application/json':
        request_data = request.get_json()
    elif request.mimetype == 'multipart/form-data':
        request_data = request.form
    else:
        return Response('Unacceptable request', status=400)
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
    # curl -X GET 'http://localhost:8080/api/user/token/check' -H "Authorization: Bearer {{TOKEN}}"
    token = request.headers.get('Authorization').replace('Bearer ', '')
    u = User().get_user_by_jwt(token)
    if u:
        return Response("Valid; Expires %s" % jwt.decode(token, verify=False)['exp'])
    else:
        return Response("Invalid", 401)

@user_api_routes.route('/token/renew', methods=['GET'])
@login_required
def token_renew():
    # curl -X GET 'http://localhost:8080/api/user/token/renew' -H "Authorization: Bearer {{TOKEN}}"
    return Response(
        response=json.dumps({'jwt_token': g.user.create_jwt()}),
        status=200,
        mimetype='application/json')