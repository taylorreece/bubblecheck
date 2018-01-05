from flask import Blueprint
from flask import render_template
from flask import request
from app import db
from app import User

import pprint
user_api_routes = Blueprint('user_api_routes', __name__)

@user_api_routes.route('/add', methods=['POST'])
def add():
    pprint.pprint(request.args)
    new_user = User(
        username = request.values.get('username'),
        teachername = request.values.get('teachername', ''),
        email = request.values.get('email'),
        is_admin = False
    )
    new_user.set_password(request.values.get('password', ''))
    db.session.add(new_user)
    db.session.commit();
    return ('', 200)
