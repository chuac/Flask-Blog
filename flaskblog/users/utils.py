import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail # no longer importing "app", using current_app as imported above


# for all the functions that were previously in flaskblog.routes.py but relate to users

# future improvements: check if picture with name of the random hex already exists in db. Unlikely but could cause issues
def save_picture(form_picture):
    random_hex = secrets.token_hex(8) # generate random hex so we don't store pics under the name the user uploaded with
    f_name, f_ext = os.path.splitext(form_picture.filename) # grab the file extension though, we need that. Python convention would be to name the name part of the split string "_" since it is not used
    new_pic_name = random_hex + f_ext # concatenate the new hex plus the file extension
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', new_pic_name)

    #form_picture.save(picture_path) # we no longer want this to save all pictures at any size the users upload to the server

    output_size = (125, 125) # our css would resize pics to 125x125px anyways
    img = Image.open(form_picture) # Image is imported from Pillow (PIL) library
    img.thumbnail(output_size)
    img.save(picture_path)

    return new_pic_name

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender = 'noreply@chuac.me', recipients = [user.email])
    msg.body = f'''To reset your password, visit the following link: {url_for('users.reset_token', token = token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
    ''' # _external gives us the full URL to the link, not just a relative path in the project
    mail.send(msg)