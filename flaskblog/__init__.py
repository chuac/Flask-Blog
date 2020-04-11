from flask import Flask #import flask library that we installed.
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config




db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login' # the 'login' is the function of our login route. same like using url_for. the users is the blueprint where the login route is
login_manager.login_message_category = 'info' #  Bootstrap for the "Login required" message

mail = Mail()



def create_app(config_class = Config): # the class we created in config.py as default. we move the initialisation into here so the extensions only need to be initialised once if we wanted to use them with multiple apps
    app = Flask(__name__) # create a flask app
    app.config.from_object(Config) # from config.py

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    from flaskblog.users.routes import users # the 'users' we are importing is the Blueprint instance initialised at the top of routes.py in th new users package
    from flaskblog.posts.routes import p as posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors

    app.register_blueprint(users) # register that blueprint
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
