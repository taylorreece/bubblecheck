from flask import Blueprint
from flask import render_template
from bubblecheck import app
import requests

default_view_routes = Blueprint('default_view_routes', __name__)

@default_view_routes.route('/', defaults={'path': ''})
@default_view_routes.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("dist/index.html")