from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

p = Blueprint('posts', __name__) # pass in the name of our blueprint too: "posts". set it to "p" here so it doesn't collide with our routes/functios


@p.route('/posts')
def posts():
    #all_posts = Post.query.order_by(Post.date_posted).all()
    page = request.args.get('page', 1, type = int) # look for optional parameter in GET request, default to 1, of type int
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page = 5) # enter page requested into our paginate query on the Post model
    return render_template('posts.html', posts = posts, title = "Posts") #you will have access in html to this posts variable

@p.route('/post/<int:id>') # View a singular post. Corey Schafer new post style.
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', title = post.title, post = post)

@p.route('/posts/<int:id>/delete', methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('posts.posts'))

@p.route('/posts/<int:id>/edit', methods=['GET', 'POST'])
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
        return redirect(url_for('posts.post', id = post.id))
    elif request.method == 'GET': # user just visited the edit page of their post so we populate the field with the current post's data
        form.title.data = post.title
        form.content.data = post.content
    return render_template('edit.html', title = 'Update Post', form = form)

@p.route('/posts/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content = form.content.data, user_id = current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("New post created", 'success')
        return redirect(url_for('posts.posts')) # giving posts.posts into url_for now. the first posts is the Blueprint, and the second is the posts function in that package's routes.py file
    else:
        return render_template('new_post.html', title = 'New Post', form = form)