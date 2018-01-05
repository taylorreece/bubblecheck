from flask import Blueprint
from flask import render_template
from flask import jsonify

from app.models import Exam
from app import db

exam_api_routes = Blueprint('exam_api_routes', __name__)
