from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from http import HTTPStatus
from models.user import User
from shared.cognito import cognito
from uuid import uuid4

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/current_user', methods=['GET'])
@login_required
def get_current_user():
    return jsonify(user=current_user.to_json(), success=True)

# Cognito will return a ?code=.... arg to this endpoint, which we can exchange for a Cognito JWT
@user_routes.route('/oauth/cognito/callback', methods=['GET'])
def login_via_cognito_callback():
    login_code = request.args.get('code')
    email = cognito.get_email_from_code(
        code=login_code, 
        callback_url=url_for(
            'user_routes.login_via_cognito_callback',
            _external=True
    ))
    if not email:
        return jsonify(error="OAuth did not return an email address property.")
    user = User(email)
    if user.exists:
        login_user(user)
        return redirect(url_for('user_routes.get_current_user'))
    else:
        _user = User(email)
        _user.email = email
        _user.id = str(uuid4())
        _user.save()
        login_user(_user)
        return redirect(url_for('user_routes.get_current_user'))

# Redirect to Cognito OAuth site
@user_routes.route('/oauth/cognito/login', methods=['GET'])
def oauth_login_redirect():
    redirect_url=cognito.cognito_login_url(
        callback_url=url_for(
            'user_routes.login_via_cognito_callback',
            _external=True
    ))
    return redirect(redirect_url)

@user_routes.route('/logout', methods=['GET'])
def user_logout_view():
    logout_user()
    return jsonify(success=True)

# Allow an app to snag an auth token and exchange it for a local JWT
@user_routes.route('/jwt/cognito/<login_code>')
def echange_cognito_code_for_jwt(login_code):
    email = cognito.get_email_from_code(
        code=login_code, 
        callback_url=url_for(
            'user_routes.login_via_cognito_callback',
            _external=True
    ))
    _user = User(email)
    if _user.exists:
        return jsonify(jwt=_user.create_jwt(), success=True)
    else:
        resp = jsonify(error='No such user found', success=False)
        resp.status_code = HTTPStatus.NOT_FOUND
        return resp