from flask import Blueprint
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
    j = request.get_json()
    new_user = User(
        teachername = j['teachername'],
        email = j['email'],
        is_admin = False
    )
    new_user.set_password(j['password'])
    db.session.add(new_user)
    db.session.commit();
    return Response(status=200)

@user_api_routes.route('/get/<userid>', methods=['GET'])
def get(userid):
    u = db.session.query(User).filter(User.id==userid).first()
    if u:
        return jsonify(u.serialize)
    else:
        return Response(status=404)

@user_api_routes.route('/token/request', methods=['POST'])
def token_login():
    j = request.get_json()
    email = j['email']
    password = j['password']
    u = db.session.query(User).filter(User.email==email).first()
    if u and u.check_password(password):
        password = u.password
        return Response(u.create_jwt(), 200)
    else:
        return ('Bad password', 401)

@user_api_routes.route('/token/check', methods=['GET'])
def token_check():
    # curl -X GET 'http://localhost:8080/api/user/token/check' -H "Authorization: Bearer {{TOKEN}}"
    token = request.headers.get('Authorization')[7:] # Strip 'Bearer '
    u = User().get_user_by_jwt(token)
    if u:
        return Response("Valid")
    else:
        return Response("Invalid", 401)
