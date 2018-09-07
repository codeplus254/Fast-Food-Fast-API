"""This python file is responsible for showing all user orders"""

from flask import Flask
from flask import request


APP = Flask(__name__)


@APP.route('/')
def index():
    """This function shows the home page of the api"""
    return 'Fast Food Fast API'


@APP.route('/api/v1/orders', methods=['GET', 'POST'])
def orders():
    """when the user of the api goes to <url>/orders s/he gets an input form"""
    """Place an order for food"""
    '''<html>
                <form method="POST" action="http://localhost:5000/api/v1/orders">
                      Food: <input type="text" name="food"><br>
                      Quantity: <input type="text" name="quantity"><br>
                      <input type="submit" value="Submit"><br>
                  </form>
            </html>''' 
    
    # treat POST request 
    # treat POST request 
    
    if request.method == 'POST':
        food = request.form['food']
        return "You've placed an order for "+food
    else:
        
        return '''<html>
                <form method="POST" action="http://localhost:5000/api/v1/orders">
                      Food: <input type="text" name="food"><br>
                      Quantity: <input type="text" name="quantity"><br>
                      <input type="submit" value="Submit"><br>
                  </form>
            </html>'''
#def test_orders(client,app):
     #assertEqual( client.get('/api/v1/orders').status_code, 400)
    
@APP.route('/api/v1/orders/<orderId>', methods=['GET', 'PUT'])
def order():
    """when the user of the api goes to <url>/orders s/he gets an input form"""
    """Place an order for food"""
    '''<html>
                <form method="POST" action="http://localhost:5000/api/v1/orders">
                      Food: <input type="text" name="food"><br>
                      Quantity: <input type="text" name="quantity"><br>
                      <input type="submit" value="Submit"><br>
                  </form>
            </html>''' 
    if request.method == 'GET':
        return "ECHO: GET\n"
