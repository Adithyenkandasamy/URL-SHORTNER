import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL','sqlite:///url_shortener.db')
print(SQLALCHEMY_DATABASE_URI)
SQALCHEMY_TRACK_MODIFICATIONs = False

ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
