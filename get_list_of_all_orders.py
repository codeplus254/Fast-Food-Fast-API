"""This python file is responsible for showing all user orders"""

from flask import Flask
#from flask import request


APP = Flask(__name__)


@APP.route('/')
def index():
    """This function shows the home page of the api"""
    return 'Fast Food Fast API'


@APP.route('/api/v1/orders', methods=['GET', 'POST'])
def orders():
    """when the user of the api goes to <url>/orders s/he gets an input form"""
    if request.method == "POST":
            
        return '''<form method="POST">
                      Food: <input type="text" name="language"><br>
                      Quantity: <input type="text" name="framework"><br>
                      <input type="submit" value="Submit"><br>
                  </form>'''
    e

def test_orders(client,app):
     assertEqual( client.get('/api/v1/orders').status_code, 400)
    
    
