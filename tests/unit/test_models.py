from flaskblog.models import User


def test_new_user(): # pytest documentation says we must start these function names like test_*():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the username, email, hashed password, image_file
    """
    new_user = User('test_username', 'testing@email.com', 'Passw0rd')
    assert new_user.username == 'test_username'
    assert new_user.email == 'testing@email.com'
    assert new_user.password != 'Passw0rd' # checking the bcrypt password hashing has worked and the hashed password (instead of the plaintext) is stored in the db
    assert new_user.image_file == "default.jpg"