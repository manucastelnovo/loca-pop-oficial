import os

SECRET_KEY='deathmaroz'
basedir=os.path.abspath(os.path.dirname(__file__))
DEBUG=True
SQLALCHEMY_DATABASE_URI='sqlite:///database.db'