from flask import Blueprint
from flask import render_template

user_api_routes = Blueprint('user_api_routes', __name__)

@user_api_routes.route('/test')
def test():
    return "Hello World from user"
