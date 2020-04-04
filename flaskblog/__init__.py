from flask import Flask #import flask library that we installed.
from flask_sqlalchemy import SQLAlchemy

#vid 1:22:59
app = Flask(__name__) # create a flask app
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = '17e7dd8d7afca3977c38e1a69a07ab45' #added secret key to help with secure cookies with user logins

from flaskblog import routes