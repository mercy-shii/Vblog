from . import main
from flask import render_template

@main.route('/')
def index():
    title = 'Hello World'
    return render_template('index.html', title=title)