from app import app
from flask import Blueprint
from flask import render_template
#from flask_login import login_required

default_web_views = Blueprint('default_web_views', __name__)

@default_web_views.route('/')
def index():
    return render_template('home.html')

@default_web_views.route('/about')
#@login_required
def about():
    return render_template('about.html')
