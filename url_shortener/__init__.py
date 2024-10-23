from flask import Flask
from .extensions import db
from .routes import short
from .models import *
from functools import wraps
from flask import request, Response, current_app

# Check if the provided username and password match the ones in the config
def check_auth(username, password):
    return username == current_app.config['ADMIN_USERNAME'] and password == current_app.config['ADMIN_PASSWORD']

# Send a 401 response to request credentials if authentication fails
def authenticate():
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

# Decorator to require authentication on certain routes
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        # If no auth is provided or if auth fails, send the authentication request
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# Factory function to create and configure the Flask app
def create_app(config_file='settings.py'):
    app = Flask(__name__)

    # Load configuration from a file
    app.config.from_pyfile(config_file)

    # Initialize database
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Register blueprint for URL shortening routes
    app.register_blueprint(short)

    # Add authentication configuration
    app.config['ADMIN_USERNAME'] = 'admin'  # Set your desired username
    app.config['ADMIN_PASSWORD'] = 'password'  # Set your desired password

    # Protected route that requires authentication
    @app.route('/protected')
    @requires_auth
    def protected():
        return "Hello, Admin!"

    return app

if __name__ == '__main__':
    # Create the Flask app and run it
    app = create_app()
    app.run(debug=True)
