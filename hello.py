from flask import Flask, render_template, request, redirect #import flask library that we installed. render_template helps use templates
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#vid 1:22:59
app = Flask(__name__) # create a flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogPost(db.Model): #each class variable is considered a piece of data in your database
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False) #cant be null, must exist
    content = db.Column(db.Text, nullable = False)
    author = db.Column(db.String(20), nullable = False, default = "N/A")
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id)

all_posts = [ #dummy data
    {
        'title': 'Post 1',
        'content': 'This is the content of post 1. Blah',
        'author': 'Chris'
    },
    {
        'title': 'Post 2',
        'content': 'This is the content of post 2. Bleh'
    }
]

@app.route('/') #define a route and code to run. this route would be at our base url. like base google.com
def index():
    return render_template('index.html')

@app.route('/posts', methods = ['GET', 'POST']) #already GET by default but now we want to allow POST too
def posts():

    if request.method == 'POST':
        post_title = request.form['title']
        post_author = request.form['author']
        post_content = request.form['content']
        new_post = BlogPost(title = post_title, content = post_content, author = post_author)
        db.session.add(new_post) #add to db in this session
        db.session.commit() #now saved permanently in the db
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts = all_posts) #you will have access in html to this posts variable

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    post = BlogPost.query.get_or_404(id)

    if request.method == 'POST':
        #post = BlogPost.query.get_or_404(id)
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post = post) #sending over the post we are editing to the html side, as variable: post

@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_author = request.form['author']
        post_content = request.form['content']
        new_post = BlogPost(title = post_title, content = post_content, author = post_author)
        db.session.add(new_post) #add to db in this session
        db.session.commit() #now saved permanently in the db
        return redirect('/posts')
    else:
        return render_template('new_post.html')


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

if __name__ == "__main__":
    app.run(debug=True)
