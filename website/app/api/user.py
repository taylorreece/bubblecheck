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

# @user_api_routes.route('/get/<userid>', methods=['GET'])
# def get(userid):
#     u = db.session.query(User).filter(User.id==userid).first()
#     if u:
#         return jsonify(u.serialize())
#     else:
#         return Response(status=404)

@user_api_routes.route('/token/request', methods=['POST'])
def token_login():
    # curl -X POST http://localhost:8080/api/user/token/request --data '{"email":"8LYEEX4H@IRLUH.com","password":"foobar123!"}' -H "Content-Type: application/json"
    j = request.get_json()
    email = j['email']
    password = j['password']
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
    return Response(
        response=json.dumps({'jwt_token': g.user.create_jwt()}),
        status=200,
        mimetype='application/json')