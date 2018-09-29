"""This python file is responsible for showing all user orders"""

from flask import Flask, request, jsonify



APP = Flask(__name__)

NAME_ERROR = {"status": "Failure", "Message":"Make a post request first"}
INDEX_ERROR = {"status": "Failure", "Message":"No such order exists! Check the order ID"}
REQUESTED_DATA = []
CURRENT_ID = 0
ALL_ORDERS, ORDER_ID, ORDER_CONTACT, ORDER_DELIVERY_ADDRESS = [], [], [], []
ORDER_NAME, ORDER_PRICE, ORDER_QUANTITY, ORDER_STATUS = [], [], [], []

@APP.route('/')
def index():
    """This function shows the home page of the api"""
    return 'Welcome to the Fast Food Fast API'
@APP.route('/api/v1/orders', methods=['GET', 'POST'])
def orders():
    """when the user of the api goes to <url>/api/v1/orders s/he gets the menu and selects.
    On submission, the user gets to see the selected items"""
    if request.method == 'POST':
        REQUESTED_DATA.append(request.get_json())     #one can make more than one post request
        global CURRENT_ID, ORDER_ID, ORDER_CONTACT, ORDER_DELIVERY_ADDRESS
        global ORDER_NAME, ORDER_PRICE, ORDER_QUANTITY, ORDER_STATUS
        for order in REQUESTED_DATA: #user should only post one order
            CURRENT_ID += 1
            ORDER_ID.append(CURRENT_ID)
            ORDER_NAME.append(order['name'])
            ORDER_PRICE.append(order['price'])
            ORDER_QUANTITY.append(order['quantity'])
            ORDER_DELIVERY_ADDRESS.append(order['address'])
            ORDER_CONTACT.append(order['contact'])
            ORDER_STATUS.append('New')
        CURRENT_ID = 0 #reset
        return jsonify({'Request_Status': 'Success',
                        'Message':'You have successfully posted this order.',
                        'order' :{'name':request.json['name'],
                                  'price':request.json['price'],
                                  'quantity' : request.json['quantity'],
                                  'address': request.json['address'],
                                  'contact':request.json['contact']}})
    #else if request.method == 'GET'
    try:
        global ALL_ORDERS
        for ids in range(1, len(ORDER_ID)+1):
            ALL_ORDERS.append({'name':ORDER_NAME[ids-1],
                               'id':ORDER_ID[ids-1],
                               'price':ORDER_PRICE[ids-1],
                               'quantity' : ORDER_QUANTITY[ids-1],
                               'address': ORDER_DELIVERY_ADDRESS[ids-1],
                               'contact':ORDER_CONTACT[ids-1],
                               'status':ORDER_STATUS[ids-1]})
    finally:
        return jsonify({'Request_Status':'Success', 
                        'Message':'You have successfully fetched all orders.',
                        'orders':ALL_ORDERS})

@APP.route('/api/v1/orders/<int:specific_order_id>', methods=['GET', 'PUT'])
def show_order(specific_order_id):
    """when the user of the api goes to <url>/api/v1/orders/<int:specific_order_id> s/he gets
    the specific order if it exists"""
    if request.method == 'GET':
        try:
            if ALL_ORDERS: #not empty
                return jsonify({'Request_Status': 'Success',
                                'Message':'You have successfully fetched the order.',
                                'order' : {'name':ORDER_NAME[specific_order_id-1],
                                           'id':ORDER_ID[specific_order_id-1],
                                           'price':ORDER_PRICE[specific_order_id-1],
                                           'quantity' : ORDER_QUANTITY[specific_order_id-1],
                                           'address': ORDER_DELIVERY_ADDRESS[specific_order_id-1],
                                           'contact':ORDER_CONTACT[specific_order_id-1],
                                           'status':ORDER_STATUS[specific_order_id-1]}})
            return jsonify(NAME_ERROR)
        except IndexError:
            return jsonify(INDEX_ERROR)
    #elif request.method == 'PUT':     #THIS UPDATES STATUS OF AN ORDER
    try:
        if ALL_ORDERS: #not empty
            possible_statuses = ["New", "Processing", "Cancelled", "Complete"]
            if request.json['status'] in possible_statuses:
                ORDER_STATUS[specific_order_id-1] = request.json['status']
                return jsonify({'Request_Status': 'Success',
                                'Message':'You have successfully updated the order.',
                                'order':{'name':ORDER_NAME[specific_order_id-1],
                                         'id':ORDER_ID[specific_order_id-1],
                                         'price':ORDER_PRICE[specific_order_id-1],
                                         'quantity' : ORDER_QUANTITY[specific_order_id-1],
                                         'address': ORDER_DELIVERY_ADDRESS[specific_order_id-1],
                                         'contact':ORDER_CONTACT[specific_order_id-1],
                                         'status':ORDER_STATUS[specific_order_id-1]}})
            return jsonify({"Request_Status": "Failure", 
                            "Message":"Please input a valid order status"})
        return jsonify(NAME_ERROR)
    except IndexError:
        return jsonify(INDEX_ERROR)