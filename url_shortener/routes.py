from flask import Blueprint,render_template,request

short = Blueprint('short', __name__)

@short.route('/<short_url>')
def redirect(short_url):
    pass

@short.route('/')
def index():
    return render_template('index.html')

@short.route('/add_link',methods=['POST'])
def add_link():
    orignal_url = request.form['orignal_url']
    link = Link(original_url=original_url)
    db.session.add(link)
    db.session.commit()

    return render_template('link_added.html',
         new_link=link.short_url,original_url=link.original_url)

@short.errorhandler(404)
def page_not_found(e):
    return '',404
