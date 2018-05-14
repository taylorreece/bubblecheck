from wtforms import BooleanField
from wtforms import FieldList
from wtforms import Form
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import StringField
from wtforms import validators
from flask_wtf import RecaptchaField

# ===================================================
class LoginForm(Form):
    ''' Form for login screen '''
    email       = StringField("Email Address", [validators.Email(message="That's not a valid email address.")])
    password    = PasswordField("Password")
    remember_me = BooleanField("Remember Me")

# ===================================================
class CourseForm(Form):
    name        = StringField("Course Name", [validators.DataRequired(message="Course name required")])
    sections    = FieldList(
        StringField("Section"),
        min_entries = 1
    )
