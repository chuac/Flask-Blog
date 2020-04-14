from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, # no-longer just importing from flaskblog.forms ... because of our new Blueprint project structure
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__) # pass in the name of our blueprint too: 'users'


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: # user is already logged in, no need to show them register page
        return redirect(url_for('posts.posts'))
    form = RegistrationForm()
    if form.validate_on_submit() and request.method == 'POST': # validate POST data
        #hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        user = User(form.username.data, form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}! You are now able to log in", 'success') # flash message, using python f-strings. 2nd arg is a "category". 'success' is Bootstrap style
        return redirect(url_for('users.login')) # is a valid form so now we redirect to posts page
    return render_template('register.html', form = form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: # user is already logged in, no need to show them login page
        return redirect(url_for('posts.posts'))
    form = LoginForm()
    if form.validate_on_submit(): # validate POST data
        user = User.query.filter_by(email=form.email.data).first() # retrieve a user in db that has same email as entered into the form
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') # capture what page the user was trying to visit before we asked them to login
            return redirect(next_page) if next_page else redirect(url_for('posts.posts'))
        else:
            flash(f"Login unsuccessful. Please check email and password", 'danger')
        #flash(f"Login successful for {form.username.data}!", 'success') # flash message, using python f-strings. 2nd arg is a "category". 'success' is Bootstrap style
        #return redirect(url_for('posts')) # is a valid form so now we redirect to posts page
    return render_template('login.html', form = form) # login unsuccessful so just return them to login page

@users.route('/logout')
def logout():
    logout_user() # imported this above, from flask_login
    return redirect(url_for('main.index'))

@users.route('/account', methods=['GET', 'POST'])
@login_required # flask_login functionality. need to tell login_manager in __init__.py where our login route is
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data: # user submitted/uploaded a picture
            picture_file_path = save_picture(form.picture.data)
            current_user.image_file = picture_file_path
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file) # find user's image file then concatenate the path to it, to be passed off to template
    return render_template('account.html', title='Account', image_file = image_file, form = form)

@users.route('/user/<string:username>') # show all the posts for a specific user
def user_posts(username):
    page = request.args.get('page', 1, type = int) # look for optional parameter in GET request, default to 1, of type int
    user = User.query.filter_by(username = username).first_or_404() # using the username variable passed to us from the route, get the first query from db, otherwise return 404
    posts = (Post.query.filter_by(author = user)
                .order_by(Post.date_posted.desc())
                .paginate(page = page, per_page = 5)
            ) # parenthesis method to break apart a long line
    return render_template('user_posts.html', posts = posts, user = user, title = "User Posts")

@users.route('/reset_password', methods=['GET', 'POST']) # enter email to submit a reset password request
def reset_request():
    if current_user.is_authenticated: # user is already logged in, no need to show them password reset request page
        return redirect(url_for('posts.posts'))

    form = RequestResetForm()

    if form.validate_on_submit(): # user entered a valid email and also one that's on the database. we now send them an email
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title = 'Reset Password', form = form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated: # user is already logged in, no need to show them password reset request page
        return redirect(url_for('posts.posts'))
    user = User.verify_reset_token(token)
    if user is None: # couldn't verify token
        flash('That is an invalid or expired token.', 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit(): # validate POST data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password # already have all their data since they're already a user. just need to update their password with a new hashed pw
        db.session.commit()
        flash(f"Your password has been updated! You are now able to log in", 'success') # flash message, using python f-strings. 2nd arg is a "category". 'success' is Bootstrap style
        return redirect(url_for('users.login')) # is a valid form so now we redirect to posts page
    return render_template('reset_token.html', title = 'Reset Password', form = form)