from flask import render_template, request, redirect, url_for, flash # render_template helps use templates
from flaskblog import app, db, bcrypt # importing from our package, __init__.py
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm #from the forms.py that we created
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image # to resize images users upload before saving
import secrets
import os

@app.route('/') #define a route and code to run. this route would be at our base url. like base google.com
def index():
    return render_template('index.html')

@app.route('/posts', methods = ['GET', 'POST']) #already GET by default but now we want to allow POST too
def posts():

    if request.method == 'POST':
        post_title = request.form['title']
        #post_author = request.form['author']
        post_content = request.form['content']
        new_post = BlogPost(title = post_title, content = post_content, user_id = "999")
        db.session.add(new_post) #add to db in this session
        db.session.commit() #now saved permanently in the db
        return redirect(url_for('posts'))
    else:
        all_posts = Post.query.order_by(Post.date_posted).all()
        return render_template('posts.html', posts = all_posts) #you will have access in html to this posts variable

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('posts'))

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    post = Post.query.get_or_404(id)

    if request.method == 'POST':
        #post = BlogPost.query.get_or_404(id)
        post.title = request.form['title']
        #post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('posts'))
    else:
        return render_template('edit.html', post = post) #sending over the post we are editing to the html side, as variable: post

@app.route('/posts/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_author = current_user.id
        post_content = request.form['content']
        new_post = Post(title = post_title, content = post_content, user_id = post_author)
        db.session.add(new_post) #add to db in this session
        db.session.commit() #now saved permanently in the db
        return redirect(url_for('posts'))
    else:
        return render_template('new_post.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: # user is already logged in, no need to show them register page
        return redirect(url_for('posts'))
    form = RegistrationForm()
    if form.validate_on_submit(): # validate POST data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}! You are now able to log in", 'success') # flash message, using python f-strings. 2nd arg is a "category". 'success' is Bootstrap style
        return redirect(url_for('login')) # is a valid form so now we redirect to posts page
    return render_template('register.html', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: # user is already logged in, no need to show them login page
        return redirect(url_for('posts'))
    form = LoginForm()
    if form.validate_on_submit(): # validate POST data
        user = User.query.filter_by(email=form.email.data).first() # retrieve a user in db that has same email as entered into the form
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') # capture what page the user was trying to visit before we asked them to login
            return redirect(next_page) if next_page else redirect(url_for('posts'))
        else:
            flash(f"Login unsuccessful. Please check email and password", 'danger')
        #flash(f"Login successful for {form.username.data}!", 'success') # flash message, using python f-strings. 2nd arg is a "category". 'success' is Bootstrap style
        #return redirect(url_for('posts')) # is a valid form so now we redirect to posts page
    return render_template('login.html', form = form) # login unsuccessful so just return them to login page

@app.route('/logout')
def logout():
    logout_user() # imported this above, from flask_login
    return redirect(url_for('index'))

# future improvements: check if picture with name of the random hex already exists in db. Unlikely but could cause issues
def save_picture(form_picture):
    random_hex = secrets.token_hex(8) # generate random hex so we don't store pics under the name the user uploaded with
    f_name, f_ext = os.path.splitext(form_picture.filename) # grab the file extension though, we need that. Python convention would be to name the name part of the split string "_" since it is not used
    new_pic_name = random_hex + f_ext # concatenate the new hex plus the file extension
    picture_path = os.path.join(app.root_path, 'static/profile_pics', new_pic_name)

    #form_picture.save(picture_path) # we no longer want this to save all pictures at any size the users upload to the server

    output_size = (125, 125) # our css would resize pics to 125x125px anyways
    img = Image.open(form_picture) # Image is imported from Pillow (PIL) library
    img.thumbnail(output_size)
    img.save(picture_path)

    return new_pic_name

@app.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file) # find user's image file then concatenate the path to it, to be passed off to template
    return render_template('account.html', title='Account', image_file = image_file, form = form)


@app.route('/home2')
@app.route('/home') #the method below is closest to this route and therefore two routes can share one method.
def hello():
    return "Hello World"

@app.route('/home/users/<string:name>/posts/<int:id>') #handle multiple URLs with one function. "Dynamic URLs"
def hi(name, id):
    return "Hello, " + name + " your id is " + str(id)

@app.route('/onlyget', methods=['GET']) #only allow GET requests
def get_only():
    return 'You can only GET this webpage'