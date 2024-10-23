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
