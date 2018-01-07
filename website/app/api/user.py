from flask import Blueprint
from flask import render_template
from flask import request
from flask import Response
from app import db
from app import User

user_api_routes = Blueprint('user_api_routes', __name__)

@user_api_routes.route('/add', methods=['POST'])
def add():
    new_user = User(
        username = request.values.get('username'),
        teachername = request.values.get('teachername', ''),
        email = request.values.get('email'),
        is_admin = False
    )
    new_user.set_password(request.values.get('password', ''))
    db.session.add(new_user)
    db.session.commit();
    return Response(status=200)
