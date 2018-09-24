"""This python file is responsible for showing all user orders"""

from flask import Flask, request, jsonify



APP = Flask(__name__)

NAME_ERROR = {'status': 'failed!', 'message':'make a post request first'}
INDEX_ERROR = {'status': 'failed!', 'message':'No such order exists! Check the order ID'}
REQUESTED_DATA = []

@APP.route('/')
def index():
    """This function shows the home page of the api"""
    return 'Fast Food Fast API'
@APP.route('/api/v1/orders', methods=['GET', 'POST'])
def orders():
    """when the user of the api goes to <url>/api/v1/orders s/he gets the menu and selects.
    On submission, the user gets to see the selected items"""
    if request.method == 'POST':
        REQUESTED_DATA.append(request.get_json())     #one can make more than one post request
        global ORDER_ID, ORDER_CONTACT, ORDER_DELIVERY_ADDRESS
        ORDER_ID, ORDER_CONTACT, ORDER_DELIVERY_ADDRESS = [], [], []
        global ORDER_NAME, ORDER_PRICE, ORDER_QUANTITY
        ORDER_NAME, ORDER_PRICE, ORDER_QUANTITY = [], [], []
        for posted_requests in REQUESTED_DATA: #REQUESTED_DATA will be a list of list
            for order in posted_requests:
                ORDER_ID.append(order['id'])
                ORDER_NAME.append(order['name'])
                ORDER_PRICE.append(order['price'])
                ORDER_QUANTITY.append(order['quantity'])
                ORDER_DELIVERY_ADDRESS.append(order['address'])
                ORDER_CONTACT.append(order['contact'])
        return jsonify({'name':ORDER_NAME, 'id':ORDER_ID, 'price':ORDER_PRICE,
                        'quantity' : ORDER_QUANTITY, 'address': ORDER_DELIVERY_ADDRESS,
                        'contact':ORDER_CONTACT})
    else:
        try:
            return jsonify({'name':ORDER_NAME, 'id':ORDER_ID, 'price':ORDER_PRICE,
                            'quantity' : ORDER_QUANTITY, 'address': ORDER_DELIVERY_ADDRESS,
                            'contact':ORDER_CONTACT})

        except NameError:
            return jsonify(NAME_ERROR)

@APP.route('/api/v1/orders/<int:specific_order_id>', methods=['GET', 'PUT'])
def show_order(specific_order_id):
    """when the user of the api goes to <url>/api/v1/orders/<int:specific_order_id> s/he gets
    the specific order if it exists"""
    if request.method == 'GET':
        try:
            if isinstance(ORDER_ID, list):

                return jsonify({'name':ORDER_NAME[specific_order_id-1],
                                'id':ORDER_ID[specific_order_id-1],
                                'price':ORDER_PRICE[specific_order_id-1],
                                'quantity' : ORDER_QUANTITY[specific_order_id-1],
                                'address': ORDER_DELIVERY_ADDRESS[specific_order_id-1],
                                'contact':ORDER_CONTACT[specific_order_id-1]})
        except NameError:
            return jsonify(NAME_ERROR)
        except IndexError:
            return jsonify(INDEX_ERROR)
    elif request.method == 'PUT':
        try:
            ORDER_NAME[specific_order_id-1] = request.json['name']
            ORDER_PRICE[specific_order_id-1] = request.json['price']
            ORDER_QUANTITY[specific_order_id-1] = request.json['quantity']
            ORDER_DELIVERY_ADDRESS[specific_order_id-1] = request.json['address']
            ORDER_CONTACT[specific_order_id-1] = request.json['contact']
            return jsonify({'name':ORDER_NAME[specific_order_id-1],
                            'id':ORDER_ID[specific_order_id-1],
                            'price':ORDER_PRICE[specific_order_id-1],
                            'quantity' : ORDER_QUANTITY[specific_order_id-1],
                            'address': ORDER_DELIVERY_ADDRESS[specific_order_id-1],
                            'contact':ORDER_CONTACT[specific_order_id-1]})
        except NameError:
            return jsonify(NAME_ERROR)
        except IndexError:
            return jsonify(INDEX_ERROR)


