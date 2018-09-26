"""This python file is responsible for creating the app"""

from flask import Flask

APP = Flask(__name__)

@APP.route('/')
def index():
    """This function shows the home page of the api"""
    return 'Welcome to the Fast Food Fast API version 2.0'