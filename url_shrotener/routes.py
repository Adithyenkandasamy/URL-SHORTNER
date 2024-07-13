from flask import Blueprint,render_template

short = Blueprint('short', __name__)

@short.route('/<short_url>')
def redirect(short_url):
    pass

@short.route('/')
def index():
    return render_template('index.html')

@short.route('/add_link',methods=['POST'])
def add_link():
    pass


@short.route('/stats')
def stats():
    pass

@short.errorhandler(404)
def page_not_found(e):
    return '',404
