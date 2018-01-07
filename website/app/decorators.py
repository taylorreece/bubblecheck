from flask import flash
from flask import g
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from functools import wraps

from app import User

# ===================================================
# TODO: Change redirects to not authorized returns
def login_required_api(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
        	flash('info|You need to log in to access ' + request.url)
        	return redirect(url_for('user.login', next=request.url))
        g.current_user.logged_in = True
        return f(*args, **kwargs)
    return decorated_function
