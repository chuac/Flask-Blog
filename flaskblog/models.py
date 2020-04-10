from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db, login_manager # no longer importing "app", doesn't exist anymore...we now use current_app
from flask import current_app
from flask_login import UserMixin #login manager needs this


@login_manager.user_loader #login manager needs this
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable = False) #max length 20, must be unique
    email = db.Column(db.String(120), unique=True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default='default.jpg') #length 20 because it'll hold the hash of their image
    password = db.Column(db.String(60), nullable = False)
    posts = db.relationship('Post', backref = 'author', lazy = True) # relationship, not a column!
    # (One to many) relationship to the 'Post' class which explains the capitalisation. 
    # Pretend like the backref is adding another column to the Post model/class. Allows access like for a post's 'author' attribute
    # lazy attribute asks SQLAlchemy to load all the posts a user has relationship to, all at once.

    def get_reset_token(self, expires_sec = 1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8') # create a token with payload of user_id, expires in 1800secs

    @staticmethod # to tell Python not to expect a self variable.
    def verify_reset_token(token): # takes a token as argument
        s = Serializer(current_app.config['SECRET_KEY']) # creates Serializer
        try: # try to load the token
            user_id = s.loads(token)['user_id']
        except: # if fail to load token, we catch the exception and return None
            return None
        return User.query.get(user_id) # successfully loaded token so now we return the User with that user_id

    def __repr__(self): #how your object is printed when it is printed out
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False) #cant be null, must exist
    content = db.Column(db.Text, nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False) # relates to the 'id' column of 'user' table (which explains the lowercase 'user')

    def __repr__(self):
        return f"Blog post('{self.title}', '{self.author.username}', '{self.date_posted}')"


class BlogPost(db.Model): #each class variable is considered a piece of data in your database
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False) #cant be null, must exist
    content = db.Column(db.Text, nullable = False)
    author = db.Column(db.String(20), nullable = False, default = "N/A")
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f"Blog post('{self.title}', '{self.author}', '{self.date_posted}')"
        #return 'Blog post ' + str(self.id) #from CleverProgramming
