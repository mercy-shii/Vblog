from .import db
from . import login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Quote:
    '''
    Quote class to hold random quote
    '''

    def __init__(self, author, quote, permalink):
        self.author = author
        self.quote = quote
        self.permalink = permalink

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255), index = True)
    email = db.Column(db.String(255), unique = True, index = True)
    password_secure = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String(255))
    blogs = db.relationship("Blog", backref= "user", lazy="dynamic")
    comments = db.relationship("Comment", backref= "user", lazy="dynamic")

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self,password):
        self.password_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_secure,password)    


    def __repr__(self):
        return f'User {self.username}'

class Blog(db.Model):
    __tablename__='blogs'

    id = db.Column(db.Integer,primary_key = True)
    blog_pic_path = db.Column(db.String(255))
    title = db.Column(db.String(255))
    message = db.Column(db.String(255))
    user_id =db.Column(db.Integer,db.ForeignKey("users.id"))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comments = db.relationship("Comment",backref = "blog",lazy = "dynamic")


    def delete_blog(self):
        db.session.delete(self)
        db.session.commit()

    def get_blog(self,id):
        blog = Blog.query.filter_by(id = self.id).first()
        comments = Comment.query.filter_by(blog_id = blog.id).order_by(Comment.posted.desc())
        return comments

class Comment(db.Model):
    __tablename__ ='comments'

    id = db.Column(db.Integer,primary_key = True)
    blog_id = db.Column(db.Integer,db.ForeignKey("blogs.id"))
    title = db.Column(db.String(255))
    comment = db.Column(db.String(255))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(blog_id = id).all()
        return comments

    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()

class Subscriber(db.Model):
    __tablename__ = 'subscribers'

    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(255))
    username = db.Column(db.String(255),index = True)



