from flask import Blueprint
from flask import flash
from flask import render_template
from flask import request

from app.forms import LoginForm
from app.models import User
from app import db

user_web_routes = Blueprint('user_web_routes', __name__)

@user_web_routes.route('/login', methods=['GET'])
def login():
    return render_template('user/login.html', form=LoginForm())

@user_web_routes.route('/login', methods=['POST'])
def login_post():
    form = LoginForm(request.form)
    print(form.validate())
    if form.validate():
        _user = db.session.query(User).filter_by(email=form.email.data).first()
        if not _user:
            flash('danger|Login Incorrect')
            return render_template('user/login.html', form=form)
        if _user.check_password(form.email.password):
            return "Success"
        else:
            return "Failure"
    else:
        return render_template('user/login.html', form=form)

@user_web_routes.route('/forgot', methods=['GET'])
def forgot_get():
    return "Hello world!"
