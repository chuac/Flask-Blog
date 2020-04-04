from flask import Flask #import flask library that we installed.
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__) # create a flask app
app.config['SECRET_KEY'] = '17e7dd8d7afca3977c38e1a69a07ab45' #added secret key to help with secure cookies with user logins
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # the 'login' is the function of our login route. same like using url_for
login_manager.login_message_category = 'info' #  Bootstrap for the "Login required" message

from flaskblog import routes