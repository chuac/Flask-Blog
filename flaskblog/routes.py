from flask import render_template, request, redirect, url_for, flash # render_template helps use templates
from flaskblog import app, db, bcrypt # importing from our package, __init__.py
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm #from the forms.py that we created
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image # to resize images users upload before saving
import secrets
import os

@app.route('/') #define a route and code to run. this route would be at our base url. like base google.com
def index():
    return render_template('index.html')

@app.route('/posts')
def posts():
    #all_posts = Post.query.order_by(Post.date_posted).all()
    page = request.args.get('page', 1, type = int) # look for optional parameter in GET request, default to 1, of type int
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page = 5) # enter page requested into our paginate query on the Post model
    return render_template('posts.html', posts = posts, title = "Posts") #you will have access in html to this posts variable

@app.route('/post/<int:id>') # View a singular post. Corey Schafer new post style.
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', title = post.title, post = post)

@app.route('/posts/<int:id>/delete', methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('posts'))

@app.route('/posts/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    form = PostForm()
    post = Post.query.get_or_404(id)
    if post.author != current_user: # the current user logged in is not the author of this post, therefore not allowed to update. throw 403 Forbidden
        abort(403) 
    if form.validate_on_submit(): # user submitted valid updated post
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', id = post.id))
    elif request.method == 'GET': # user just visited the edit page of their post so we populate the field with the current post's data
        form.title.data = post.title
        form.content.data = post.content
    return render_template('edit.html', title = 'Update Post', form = form)

@app.route('/posts/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content = form.content.data, user_id = current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("New post created", 'success')
        return redirect(url_for('posts'))
    else:
        return render_template('new_post.html', title = 'New Post', form = form)

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

@app.route('/user/<string:username>') # show all the posts for a specific user
def user_posts(username):
    page = request.args.get('page', 1, type = int) # look for optional parameter in GET request, default to 1, of type int
    user = User.query.filter_by(username = username).first_or_404() # using the username variable passed to us from the route, get the first query from db, otherwise return 404
    posts = (Post.query.filter_by(author = user)
                .order_by(Post.date_posted.desc())
                .paginate(page = page, per_page = 5)
            ) # parenthesis method to break apart a long line
    return render_template('user_posts.html', posts = posts, user = user, title = "User Posts")