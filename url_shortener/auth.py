from functools import wraps
from flask import request, Response,current_app

def check_auth(username, password):
    return username == current_app.config ['ADMIN_USERNAME']  \
    and password == current_app.config['ADMIN_PASSWORD']

def authenticate():
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})   

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        print(auth)
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated