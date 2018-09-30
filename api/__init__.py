"""This python file is responsible for creating the app"""

from flask import Flask

APP = Flask(__name__)

from api.v1.routes import mod 
from api.v2.routes import mod


#APP.register_blueprint(v1.routes.mod, url_prefix = '/api/v1')
APP.register_blueprint(v2.routes.mod, url_prefix = '/api/v2')