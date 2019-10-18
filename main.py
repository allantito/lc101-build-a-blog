from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:bocaboca@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# class Task(db.Model):

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120))
#     completed = db.Column(db.Boolean)

#     def __init__(self, name):
#         self.name = name
#         self.completed = False

## New Class: Blog
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/') # To go back to main page
def index():
    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)

@app.route('/newpost')
def display():
    return render_template('newpost.html', title="New Post")

@app.route('/newpost', methods=['POST'])
def validate():

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        blog_newpost = Blog(blog_title, blog_body)

        title_error = ''
        body_error = ''

        if title_error or body_error:
            return render_template('newpost.html', title_error=title_error, body_error=body_error,
            title=blog_title, body=blog_body)
        else:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blogpost?blog_id=' + str(new_blog.id))


@app.route('/blog')
def homepage():
    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)

@app.route('/blogpost')
def blog():
    blogId = request.args.get('blog_id')
    
    blogpost = Blog.query.filter(Blog.id == blogId).first()
    return render_template('blogpost.html', blogpost=blogpost)



if __name__ == '__main__':
    app.run()