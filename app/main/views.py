from . import main
from flask import render_template,request,url_for,redirect,abort
from .. request import get_quote
from flask_login import login_required,current_user
from ..models import User,Comment,Blog,Subscriber
from .forms import BlogForm,CommentForm,UpdateProfile
from .. import db
@main.route('/')
def index():

    title = 'Developer Blog'
    quote = get_quote()
    blogs = Blog.query.all()
    
    return render_template('index.html', title=title,quote = quote,blogs = blogs)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    blogs = Blog.query.filter_by(user_id = user.id).order_by(Blog.date_posted.desc())

    if user is None:
        abort(404)

    return render_template('profile/profile.html',user = user,blogs =blogs)

@main.route('/user/<uname>/delete/<blog_id>')
@login_required
def del_blog(uname,blog_id):
    user = User.query.filter_by(username = uname).first()
    blogs = Blog.query.filter_by(user_id = user.id).order_by(Blog.date_posted.desc())
    blog = Blog.query.filter_by(id = blog_id).first()

    if blog.user_id == current_user.id:
        blog.delete_blog()

    return render_template("profile/profile.html",user = user,blogs = blogs) 

@main.route('/user/<uname>/update',methods = ['GET','POST'])  
@login_required
def update_profile(uname):
     user = User.query.filter_by(username = uname).first()
     if user is None:
         abort(404)
         
     form = UpdateProfile()

     if form.validate_on_submit():
          user.bio = form.bio.data

          db.session.add(user)
          db.session.commit()

          return redirect(url_for('.profile',uname = user.username))

     return render_template('profile/update.html',form = form,user = user)

@main.route('/user/<uname>/blog',methods =['GET','POST'])
@login_required
def new_blog(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = BlogForm()
    blog = Blog()

    if form.validate_on_submit():
        blog.title = form.title.data
        blog.message = form.message.data
        blog.user_id = current_user.id

        db.session.add(blog)
        db.session.commit()

        Subscribers = Subscriber.query.all()
       # mail_message("New Blog Post", "email/new_blog", subscriber.email, subscriber = subscriber)

        return redirect(url_for('.profile',uname=user.username))

    return render_template('new_blog.html',uname=uname, user = user, BlogForm = form)

@main.route('/comments/<blog_id>')
@login_required
def comments(blog_id):
    blog = Blog.query.filter_by(id = blog_id).first()
    comments = Comment.query.filter_by(blog_id = blog.id).order_by()


    return render_template('comments.html', blog = blog, comments = comments)

@main.route('/comment/delete/<blog_id>/<comment_id>')
@login_required
def del_comment(blog_id, comment_id):
    blog = Blog.query.filter_by(id = blog_id).first()
    comments = Comment.query.filter_by(blog_id = blog.id).order_by()
    comment = Comment.query.filter_by(id = comment_id).first()
    if blog.user_id == current_user.id or comment.user_id == current_user.id:

        Comment.delete_comment(comment)

    return render_template('comments.html', blog = blog, comments = comments)

@main.route('/blog/comment/new/<blog_id>', methods = ['GET', 'POST'])
@login_required
def new_review(blog_id):
    form = CommentForm()
    blog = Blog.query.filter_by(id = blog_id).first()
    comment = Comment()

    if form.validate_on_submit():
        comment.title = form.title.data
        comment.comment = form.comment.data
        comment.blog_id = blog_id
        comment.user_id = current_user.id

        db.session.add(comment)
        db.session.commit()

        return redirect(url_for('main.comments', blog_id=blog.id ))

    return render_template('new_comment.html', comment_form = form)    