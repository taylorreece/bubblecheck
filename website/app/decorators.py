from flask import flash
from flask import g
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from functools import wraps

from app.models import User

# ===================================================
def login_required_api(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        g.current_user = None
        if 'sessionid' in session:
            g.current_user = User.getUserBySessionID(str(session['sessionid']))
        if request.values.get('apikey'):
            g.current_user = User.getUserByAPIKey(str(request.values.get('api_key')))
        if g.current_user is None:
        	return ("You need to log in to do that.", 403)
        g.current_user.logged_in = True
        return f(*args, **kwargs)
    return decorated_function
