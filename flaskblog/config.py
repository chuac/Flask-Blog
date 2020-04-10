import os


class Config:
    SECRET_KEY = os.environ.get('PY_SECRET_KEY') #added secret key to help with secure cookies with user logins
    SQLALCHEMY_DATABASE_URI = os.environ.get('PY_SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('PY_EMAIL_USER') # my gmail details set in Windows Environment Variables. Gmail "less secure app access" also allowed
    MAIL_PASSWORD = os.environ.get('PY_EMAIL_PASSWORD')