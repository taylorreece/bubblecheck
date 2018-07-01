from flask import Blueprint
from flask import render_template

default_view_routes = Blueprint('default_view_routes', __name__)

@default_view_routes.route('/')
def default_view_home():
    return render_template('home.html')