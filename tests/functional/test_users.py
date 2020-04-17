"""
This file (test_users.py) contains the functional tests for the users blueprint.

These tests use GETs and POSTs to different URLs to check for the proper behavior
of the users blueprint.
"""


def test_index_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Home Page" in response.data # b string literal means looking for the bytes in the response page the server sends us
    assert b"Go to Posts" in response.data

def test_index_page_post(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """
    response = test_client.post('/')
    assert response.status_code == 405
    assert b"Home Page" not in response.data
    assert b"Go to Posts" not in response.data

def test_login_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"Email" in response.data
    assert b"Password" in response.data
    assert b"Don't have an account?" in response.data

def test_valid_login_logout(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/login',
                                data = dict(username = 'user2', email = 'john_doe@user2.com',
                                password = 'Test123!'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"+ New Post" in response.data
    assert b"Logout" in response.data
    assert b"Login" not in response.data
    assert b"Register" not in response.data

    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome" in response.data
    assert b"Home Page" in response.data
    assert b"Logout" not in response.data
    assert b"Login" in response.data
    assert b"Register" in response.data

def test_invalid_login(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to with invalid credentials (POST) (valid credentials specified in TestConfig class)
    THEN check the an error message is returned to the user
    """
    response = test_client.post('/login',
                                data = dict(username = 'user2', email = 'john_doe@user2.com',
                                password = 'incorrectPassword'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Login unsuccessful. Please check email and password" in response.data
    assert b"Login" in response.data
    assert b"+ New Post" not in response.data
    assert b"Logout" not in response.data

def test_valid_registration(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/register' page is posted to (POST)
    THEN check the response is valid and the user is logged in
    """
    response = test_client.post('/register',
                                data=dict(username = 'BobDole',
                                        email='bobby@yahoo.com',
                                        password='FlaskIsGreat',
                                        confirm_password='FlaskIsGreat'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Account created for BobDole! You are now able to log in " in response.data
    assert b"Login" in response.data
    assert b"+ New Post" not in response.data

    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome" in response.data
    assert b"Home Page" in response.data
    assert b"Logout" not in response.data
    assert b"Login" in response.data
    assert b"Register" in response.data

def test_invalid_registration(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/register' page is posted to with invalid credentials (POST)
    THEN check an error message is returned to the user
    """
    response = test_client.post('/register',
                                data=dict(username = 'BobDole',
                                        email='bobby@yahoo.com',
                                        password='FlaskIsGreat',
                                        confirm_password='TotallyDiffPassword'), # the second password entered by the test client is totally different, so we expect a denied registration
                                follow_redirects=True)
    assert response.status_code == 200
    assert b"Field must be equal to password." in response.data
    assert b"Account created for BobDole! You are now able to log in " not in response.data
    assert b"Register" in response.data
    assert b"+ New Post" not in response.data