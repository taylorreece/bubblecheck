from wtforms import BooleanField
from wtforms import FieldList
from wtforms import Form
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import StringField
from wtforms import validators

# ===================================================
class LoginForm(Form):
    ''' Form for login screen '''
    email       = StringField("Email Address", [validators.Email(message=u"That's not a valid email address.")])
    password    = PasswordField("Password")
    remember_me = BooleanField(u'Remember Me')