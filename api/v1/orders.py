"""This python file is responsible for showing all user orders"""

from flask import Flask,request,send_file
import pytest


APP = Flask(__name__)
 

@APP.route('/')
def index():
    """This function shows the home page of the api"""
    return 'Fast Food Fast API'
@APP.route('/api/v1/images/<imageId>')
def get_image(imageId):
    """This function gets food icons"""
    return send_file('images/'+imageId, mimetype='image/jpeg')


@APP.route('/api/v1/orders', methods=['GET', 'POST'])
def orders():
    """when the user of the api goes to <url>/api/v1/orders s/he gets the menu and selects. On submission, the user gets to see the selected items"""
 
    # treat POST request 
    # treat POST request 
    
    if request.method == 'POST':
     
        #append the orders to a list if they've been selected
        global my_orders
        my_orders = request.form.getlist('food')
        
        return "You've order for: "+', '.join(my_orders)     #prints out the list values on html
    elif request.method == 'GET':
        
        return '''<html>
                    <form method="POST" >
                        <h3> Place your order for food </h3>
                        <input type="checkbox" name="food" value="Burger and Hamketchup" ><input type="image" src="images/burger_and_hamketchup.jpeg" alt="Burger and Hamketchup" width="100px" height="50px"> Burger and Hamketchup<br>
                            <input type="checkbox" name="food" value="Five Bake Donuts" ><input type="image" src="images/five_bake_donuts.jpeg" alt="Five Bake Donuts" width="100px" height="50px" > Five Bake Donuts<br>
                            <input type="checkbox" name="food" value="Fresh Salad" ><input type="image" src="images/fresh_salad.jpeg" alt="Fresh Salad" width="100px" height="50px" >Fresh Salad<br>
                            <input type="checkbox" name="food" value="Fried Meat" ><input type="image" src="images/fried_meat.jpeg" alt="Fried Meat" width="100px" height="50px">Fried Meat<br>
                            <input type="checkbox" name="food" value="Fries and Burger" ><input type="image" src="images/fries_and_burger.jpeg" alt="Fries and Burger" width="100px" height="50px">Fries and Burger<br>
                            <input type="checkbox" name="food" value="Hamburger" ><input type="image" src="images/hamburger.jpeg" alt="Hamburger" width="100px" height="50px">Hamburger<br>
                            <input type="checkbox" name="food" value="Healthy Burger" ><input type="image" src="images/healthy_burger.jpeg" alt="Healthy Burger" width="100px" height="50px">Healthy Burger<br>
                            <input type="checkbox" name="food" value="Meat Burger" ><input type="image" src="images/meat_burger.jpg" alt="Meat Burger" width="100px" height="50px">Meat Burger<br>
                            <input type="checkbox" name="food" value="Pizza with egg" ><input type="image" src="images/pizza_with_egg.jpeg" alt="Pizza with egg" width="100px" height="50px">Pizza with egg<br>
                            <input type="checkbox" name="food" value="Popcorn" ><input type="image" src="images/popcorn.jpeg" alt="Popcorn" width="100px" height="50px">Popcorn<br>
                            <input type="checkbox" name="food" value="Sliced Cheeseburger" ><input type="image" src="images/sliced_cheeseburger.jpeg" alt="Sliced Cheeseburger" width="100px" height="50px">Sliced Cheeseburger<br>
                            <input type="checkbox" name="food" value="Pepperoni Pizza" ><input type="image" src="images/pepperoni_pizza.jpeg" alt="Pepperoni Pizza" width="100px" height="50px">Pepperoni Pizza<br>

                        <input type="submit" value="Submit"><br>
                    </form>
                </html>''' 
        
#def test_orders(client,app):
     #assertEqual( client.get('/api/v1/orders').status_code, 400)
    
@APP.route('/api/v1/orders/<int:orderId>', methods=['GET', 'PUT','POST'])
def show_order(orderId):
    """when the user of the api goes to <url>/api/v1/orders/<int:orderId> s/he gets the specific order if it exists"""
    
    if request.method == 'PUT' or request.method == 'POST':
        my_status = request.form.getlist('status') 
        if (str(my_status)=="['confirm']"):
            return "Order ID: "+str(orderId)+ "  " + my_orders[orderId-1] + " Confirmed"
        else:
            del my_orders[orderId-1]
            return "Order ID: "+str(orderId)+ "   rejected"
    elif request.method == 'GET':
        #first check if orderId is in list. OrderId will be the index of list +1 since list index start from zero
        try:
            if (orderId<=len(my_orders)):     #ensure orderId is within range
                return '''<html>
                            <form method="POST" >
                                <h3> Please confirm or reject the order first </h3><br>
                                <input type="radio" name="status" value="confirm" checked/>
                                <label for="confirm">Confirm</label><br>
                                <input type="radio" name="status" value="reject" />
                                <label for="reject">Reject</label><br>

                                
                                <input type="submit" value="Submit"><br>
                            </form>
                        </html> '''
        #if the orderId is not in range 
        except IndexError:
            return "No such order exists!"
        else:
            return "Invalid! Please check your order id"
    
        
def test_app(client):
    response = client.get('/api/v1/orders')
    assert response.status_code == 200


def test_specific_order(client):
    response = client.get('/api/v1/orders/1')
    assert response.status_code == 200




def test_invalid_order_id(client):
    response = client.get('api/v1/orders/300')
    assert b'Invalid! Please check your order id' in response.data
