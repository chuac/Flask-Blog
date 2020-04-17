# here we create two fixtures to set up a functioning Flask app with db
# do this before we start writing functional tests (in test_users.py)
# requires Application Factory project setup, like we have here
import pytest
from flaskblog import create_app, db
from flaskblog.models import User, Post
from flaskblog.config import TestConfig



@pytest.fixture(scope='module')
def new_user(): # now we won't need to initialise new user by ourselfs in test_models.py
    new_user = User('test_username', 'testing@email.com', 'Passw0rd')
    return new_user

@pytest.fixture(scope='module')
def new_post(): # now we won't need to initialise new post by ourselfs in test_models.py
    new_post = Post('Test post title', 'Test Test Test Content', 2)
    return new_post

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(TestConfig) # the TestConfig class in our config.py

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()

@pytest.fixture(scope='module')
def init_database():
    # Create the database and the database table
    db.create_all()

    # Insert user data. Two users for us to test with in our functional tests
    user1 = User('test_username1', 'testing@email.com', 'Passw0rd')
    user2 = User('user2', 'john_doe@user2.com', 'Test123!')
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes for the users
    db.session.commit()

    yield db  # this is where the testing happens!

    db.drop_all()
