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

@user_web_routes.route('/login', methods=['GET'])
def login():
    return render_template('user/login.html', form=LoginForm())

@user_web_routes.route('/login', methods=['POST'])
def login_post():
    # TODO: No need for validating the form for login?
    form = LoginForm(request.form)
    if form.validate():
        _user = db.session.query(User).filter_by(email=form.email.data).first()
        if _user and _user.check_password(form.password.data):
            login_user(_user)
            return redirect(url_for('user_web_routes.dashboard'))
        else:
            flash('Login Incorrect', 'error')
            return render_template('user/login.html', form=form), 401
    else:
        flash('Form invalid', 'error')
        return render_template('user/login.html', form=form)

@user_web_routes.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('user_web_routes.login'))

@user_web_routes.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return "You're logged in as {}".format(current_user.email)

@user_web_routes.route('/forgot', methods=['GET'])
def forgot():
    return "stub"

@user_web_routes.route('/testlogin', methods=['GET'])
@login_required
def testlogin():
    return "You are logged in.", 200
