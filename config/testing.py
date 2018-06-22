import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

DEBUG = True
ENV = 'development'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
DATABASE_CONNECT_OPTIONS = {}
# Echo out every SQL transaction
#SQLALCHEMY_ECHO = True

# Set to 2 threads per processor core
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"