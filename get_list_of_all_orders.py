"""This python file is responsible for showing all user orders"""

from flask import Flask
from flask import request,send_file


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
                <form method="POST" action="https://fast-food-fast-api-v1.herokuapp.com/api/v1/orders">
                    <h3> Place your order for food </h3>
                    <select name= "order1">
                        <option value=" " > </option>
                        <option value="Burger and Hamketchup">Burger and Hamketchup</option>
                        <option value="Five Bake Donuts">Five Bake Donuts</option>
                        <option value="Fresh Salad">Fresh Salad</option>
                        <option value="Fried Meat">Fried Meat</option>
                        <option value="Fries and Burger">Fries and Burger</option>
                    </select><br>
                    <select name= "order2">
                        <option value=" " > </option>
                        <option value="Burger and Hamketchup">Burger and Hamketchup</option>
                        <option value="Five Bake Donuts">Five Bake Donuts</option>
                        <option value="Fresh Salad">Fresh Salad</option>
                        <option value="Fried Meat">Fried Meat</option>
                        <option value="Fries and Burger">Fries and Burger</option>
                    </select><br>
                    <select name= "order3">
                        <option value=" " > </option>
                        <option value="Burger and Hamketchup">Burger and Hamketchup</option>
                        <option value="Five Bake Donuts">Five Bake Donuts</option>
                        <option value="Fresh Salad">Fresh Salad</option>
                        <option value="Fried Meat">Fried Meat</option>
                        <option value="Fries and Burger">Fries and Burger</option>
                    </select><br>
                    <select name= "order4">
                        <option value=" " > </option>
                        <option value="Burger and Hamketchup">Burger and Hamketchup</option>
                        <option value="Five Bake Donuts">Five Bake Donuts</option>
                        <option value="Fresh Salad">Fresh Salad</option>
                        <option value="Fried Meat">Fried Meat</option>
                        <option value="Fries and Burger">Fries and Burger</option>
                    </select><br>
                    <select name= "order5">
                        <option value=" " > </option>
                        <option value="Burger and Hamketchup">Burger and Hamketchup</option>
                        <option value="Five Bake Donuts">Five Bake Donuts</option>
                        <option value="Fresh Salad">Fresh Salad</option>
                        <option value="Fried Meat">Fried Meat</option>
                        <option value="Fries and Burger">Fries and Burger</option>
                    </select><br>
                      <input type="submit" value="Submit"><br>
                  </form>
            </html>''' 
    
    # treat POST request 
    # treat POST request 
    
    if request.method == 'POST':
        global order1
        order1 = request.form.get('order1')
        global order2
        order2 = request.form.get('order2')
        global order3
        order3 = request.form.get('order3')
        global order4
        order4 = request.form.get('order4')
        global order5
        order5 = request.form.get('order5')

        return "You've ordered for: "+order1 + ", "+order2 + ", "+order3 + ", "+order4 + ", "+order5 + "."
    else:
        
        return '''<html>
                <form method="POST" action="https://fast-food-fast-api-v1.herokuapp.com/api/v1/orders">
                    <h3> Place your order for food </h3>
                    <select name= "order1">
                        <option value=" " > </option>
                        <option value="Burger and Hamketchup">Burger and Hamketchup</option>
                        <option value="Five Bake Donuts">Five Bake Donuts</option>
                        <option value="Fresh Salad">Fresh Salad</option>
                        <option value="Fried Meat">Fried Meat</option>
                        <option value="Fries and Burger">Fries and Burger</option>
                    </select><br>
                    <select name= "order2">
                        <option value=" " > </option>
                        <option value="Burger and Hamketchup">Burger and Hamketchup</option>
                        <option value="Five Bake Donuts">Five Bake Donuts</option>
                        <option value="Fresh Salad">Fresh Salad</option>
                        <option value="Fried Meat">Fried Meat</option>
                        <option value="Fries and Burger">Fries and Burger</option>
                    </select><br>
                    <select name= "order3">
                        <option value=" " > </option>
                        <option value="Burger and Hamketchup">Burger and Hamketchup</option>
                        <option value="Five Bake Donuts">Five Bake Donuts</option>
                        <option value="Fresh Salad">Fresh Salad</option>
                        <option value="Fried Meat">Fried Meat</option>
                        <option value="Fries and Burger">Fries and Burger</option>
                    </select><br>
                    <select name= "order4">
                        <option value=" " > </option>
                        <option value="Burger and Hamketchup">Burger and Hamketchup</option>
                        <option value="Five Bake Donuts">Five Bake Donuts</option>
                        <option value="Fresh Salad">Fresh Salad</option>
                        <option value="Fried Meat">Fried Meat</option>
                        <option value="Fries and Burger">Fries and Burger</option>
                    </select><br>
                    <select name= "order5">
                        <option value=" " > </option>
                        <option value="Burger and Hamketchup">Burger and Hamketchup</option>
                        <option value="Five Bake Donuts">Five Bake Donuts</option>
                        <option value="Fresh Salad">Fresh Salad</option>
                        <option value="Fried Meat">Fried Meat</option>
                        <option value="Fries and Burger">Fries and Burger</option>
                    </select><br>
                    <input type="submit" value="Submit"><br>
                  </form>
            </html>'''
#def test_orders(client,app):
     #assertEqual( client.get('/api/v1/orders').status_code, 400)
    
@APP.route('/api/v1/orders/<int:orderId>', methods=['GET', 'PUT'])
def show_order(orderId):
    """when the user of the api goes to <url>/orders s/he gets an input form"""
    """Place an order for food"""
    '''<html>
        <form method="POST" action="https://fast-food-fast-api-v1.herokuapp.com/api/v1/orders/<int:orderId>">
            <input type="hidden" name="_METHOD" value="PUT"/>
            <h3> Confirm / Reject Order </h3>
                    <select name= "change">
        
                        
                        <option value="Confirm">Confirm</option>
                        <option value="Reject">Reject</option>
                    </select><br>
                    <input type="submit" value="Submit"><br>
        </form>
        </html>'''
    if request.method == 'GET':
       
        if orderId==1:
            try: 

                if order1 == " ":
                    return "No order filled"
                else: 
                    return order1
            except NameError:
                return "Order not yet filled"
        elif orderId==2:
            try: 
                if order2 == " ":
                    return "No order filled"
                else: 
                    return order2
            except NameError:
                return "Order not yet filled"
        elif orderId==3:
            try:
                if order3 == " ":
                    return "No order filled"
                else: 
                    return order3
            except NameError:
                return "Order not yet filled"
        elif orderId==4:
            try:
                if order2 == " ":
                    return "No order filled"
                else: 
                    return order4
            except NameError:
                return "Order not yet filled"
        elif orderId==5:
            try:
                if order2 == " ":
                    return "No order filled"
                else: 
                    return order5
            except NameError:
                return "Order not yet filled"
        else:
            return "Invalid! Please check your order id"
    elif request.method == 'PUT':   
        return "Put request filed"
        
def test_app(client):
    response = client.get('/api/v1/orders')
    assert response.status_code == 200

def test_specific_order(client):
    response = client.get('/api/v1/orders/1')
    assert response.status_code == 200

def test_invalid_order_id(client):
    response = client.get('api/v1/orders/300')
    assert b'Invalid! Please check your order id' in response.data
