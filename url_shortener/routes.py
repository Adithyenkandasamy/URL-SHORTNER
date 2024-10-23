from flask import Blueprint, render_template, request, redirect, flash
from .extensions import db
from .auth import requires_auth
from .models import Link

short = Blueprint('short', __name__)

# Route to handle redirects to the original URL based on short_url
@short.route('/<short_url>')
def redirect_to_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first_or_404()
    link.visits += 1
    db.session.commit()
    return redirect(link.original_url)

# Home route with authentication
@short.route('/')
@requires_auth
def index():
    return render_template('index.html')

# Route to add a new shortened URL, with support for custom slugs
@short.route('/add_link', methods=['POST'])
@requires_auth
def add_link():
    original_url = request.form['original_url']
    custom_short_url = request.form.get('custom_short_url')

    if custom_short_url:
        existing_link = Link.query.filter_by(short_url=custom_short_url).first()
        if existing_link:
            flash('This custom short URL is already taken. Please choose another one.')
            return redirect('/')
    else:
        custom_short_url = generate_random_short_url()

    new_link = Link(original_url=original_url, short_url=custom_short_url)
    db.session.add(new_link)
    db.session.commit()
    
    return render_template('link_added.html', new_link=new_link.short_url, original_url=new_link.original_url)

# Statistics route to display all shortened URLs and their stats
@short.route('/stats')
@requires_auth
def stats():
    links = Link.query.all()
    return render_template('stats.html', links=links)

# Error handler for 404 not found
@short.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Helper function to generate a random short URL
def generate_random_short_url():
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))
