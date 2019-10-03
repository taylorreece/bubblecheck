#!/usr/bin/env python3

from app import app, migrate
from flask_migrate import upgrade
from database import db
with app.app_context():
    upgrade()
app.run(host='0.0.0.0')