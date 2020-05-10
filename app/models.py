from .import db
from . import login_manager
class Quote:
    '''
    Quote class to hold random quote
    '''

    def __init__(self, author, quote, permalink):
        self.author = author
        self.quote = quote
        self.permalink = permalink

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255), index = True)
    email = db.Column(db.String(255), unique = True, index = True)
    password = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String(255))
    #blogs = db.relationship("Blog", backref= "user", lazy="dynamic")
    #comments = db.relationship("Comment", backref= "user", lazy="dynamic")


    def __repr__(self):
        return f'User {self.username}'

