from . import main
from flask import render_template,request,url_for
from .. request import get_quote
from flask_login import login_required,current_user
from ..models import User,Comment,Blog,Subscriber
@main.route('/')
def index():

    title = 'Home - Blog'
    quote = get_quote()
    
    return render_template('index.html', title=title,quote = quote)