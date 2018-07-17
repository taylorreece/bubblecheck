import json

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import Response
from flask import url_for

from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from bubblecheck.forms import LoginForm
from bubblecheck.models import User
from bubblecheck import db

user_web_routes = Blueprint('user_web_routes', __name__)

@user_web_routes.route('/login', methods=['POST'])
def user_login_view():
    form = LoginForm(request.form)
    if form.validate():
        u = User.query.filter(User.email==form.email.data).one_or_none()
        if u and u.check_password(form.password.data):
            login_user(u)
            return redirect('/')
    flash('Login Incorrect', 'error')
    return redirect('/login')

@user_web_routes.route('/logout', methods=['GET'])
def user_logout_view():
    logout_user()
    return redirect('/')

@user_web_routes.route('/testlogin', methods=['GET'])
@login_required
def user_testlogin_view():
    return "You are logged in as {}".format(current_user.email), 200
