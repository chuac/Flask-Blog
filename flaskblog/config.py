import os


class Config:
    SECRET_KEY = os.environ.get('PY_SECRET_KEY') #added secret key to help with secure cookies with user logins
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db' # changed to DATABASE_URL for Heroku
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('PY_EMAIL_USER') # my gmail details set in Windows Environment Variables. Gmail "less secure app access" also allowed
    MAIL_PASSWORD = os.environ.get('PY_EMAIL_PASSWORD')

class TestConfig:
    # Get the folder of the top-level directory of this project
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    # Update later by using a random number generator and moving
    # the actual key outside of the source code under version control
    SECRET_KEY = 'bad_secret_key'
    DEBUG = True

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app_test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Bcrypt algorithm hashing rounds (reduced for testing purposes only!)
    BCRYPT_LOG_ROUNDS = 4

    # Enable the TESTING flag to disable the error catching during request handling
    # so that you get better error reports when performing test requests against the application.
    TESTING = True

    # Disable CSRF tokens in the Forms (only valid for testing purposes!)
    WTF_CSRF_ENABLED = False