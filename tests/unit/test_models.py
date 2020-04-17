from datetime import datetime
from flaskblog.models import User, Post


def test_new_user(new_user): # pytest documentation says we must start these function names like test_*():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the username, email, if password was hashed, image_file
    """
    assert new_user.username == 'test_username'
    assert new_user.email == 'testing@email.com'
    assert new_user.password != 'Passw0rd' # checking the bcrypt password hashing has worked and the hashed password (instead of the plaintext) is stored in the db
    assert new_user.image_file == "default.jpg"

def test_new_post(new_post):
    """
    GIVEN a Post model
    WHEN a new Post is created
    THEN check the title, content, date_posted, user_id
    """
    assert new_post.title == 'Test post title'
    assert new_post.content == 'Test Test Test Content'
    assert new_post.date_posted != datetime.utcnow # checking the date posted was in the past (ie, NOT now), as it should be
    assert new_post.user_id == 2