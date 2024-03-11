from flask import render_template
from app.main import bp

@bp.route('/')
def index():
    return 'Hello, World!'

@bp.route('/test')
def check():
    return render_template('index.html')