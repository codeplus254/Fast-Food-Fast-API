"""This python file is responsible for creating the app"""
import os
import sys
sys.path.insert(0,r'C:\Users\Ronny\fast-food-fast')
from flask import Flask
#from flask_cors import CORS
from config import app_config
from api.v1.views import mod 
from api.v2.views import mod
from api.v2.init_db import *





def create_app(config_name):
    #APP = Flask(__name__, instance_relative_config=True)
    APP = Flask(__name__)
    configuration = app_config[config_name]()
    #cors = CORS(APP)
    #APP.config['CORS_HEADERS'] = 'Content-Type'
    APP.config.from_object(configuration)
    os.environ['DATABASENAME'] = configuration.database
    create_tables()
    create_admin()
    APP.register_blueprint(v1.views.mod, url_prefix = '/api/v1')
    APP.register_blueprint(v2.views.mod, url_prefix = '/api/v2')

    return APP
