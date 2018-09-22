"""This python file is responsible for showing all user orders"""

from flask import Flask,request,send_file,jsonify
import pytest


APP = Flask(__name__)



@APP.route('/')
def index():
    """This function shows the home page of the api"""
    return 'Fast Food Fast API'
@APP.route('/api/v1/orders', methods=['GET', 'POST'])
def orders():
    """when the user of the api goes to <url>/api/v1/orders s/he gets the menu and selects. On submission, the user gets to see the selected items"""
 
    # treat POST request 
    if request.method == 'POST':
        global data,order_id,order_name,order_price,order_quantity,order_delivery_address,order_contact
        data = request.get_json()
        order_id = []
        order_id.append(data['id']) 
        order_name = []
        order_name.append(data['name'])
        order_price = []
        order_price.append(data['price'])
        order_quantity = []
        order_quantity.append(data['quantity'])
        order_delivery_address = []
        order_delivery_address.append(data['address'])
        order_contact = []
        order_contact.append(data['contact'])
        #return jsonify({'result': 'success'})
        return jsonify({'name':order_name,'id':order_id,'price':order_price,'quantity' : order_quantity,'address': order_delivery_address,'contact':order_contact})
    elif request.method == 'GET':
        #data ={"id": "24", "price": "12.00","time": "1300h","address": "Nairobi CBD"}
        try: 
           return jsonify({'name':order_name,'id':order_id,'price':order_price,'quantity' : order_quantity,'address': order_delivery_address,'contact':order_contact})

        except NameError:
            return jsonify({'status': 'failed!', 'message':'make a post request first'})

@APP.route('/api/v1/orders/<int:orderId>', methods=['GET', 'PUT'])
def show_order(orderId):
    """when the user of the api goes to <url>/api/v1/orders/<int:orderId> s/he gets the specific order if it exists"""
    if request.method == 'GET':
        try:
            if type(order_id) == list:

                return jsonify({'name':order_name[orderId-1],'id':order_id[orderId-1],'price':order_price[orderId-1],'quantity' : order_quantity[orderId-1],'address': order_delivery_address[orderId-1],'contact':order_contact[orderId-1]})
        except TypeError:   #incase the order posted is just one hencenot subscriptable
            
            return jsonify({'name':order_name,'id':order_id,'price':order_price,'quantity' : order_quantity,'address': order_delivery_address,'contact':order_contact})
        except NameError:
            return jsonify({'status': 'failed!', 'message':'make a post request first'})
        except IndexError:
            return jsonify({'status': 'failed!', 'message':'No such order exists! Check the order ID'})
    elif request.method == 'PUT':
        try:
            order_name[orderId-1] = request.json['name']
            order_price[orderId-1] = request.json['price']
            order_quantity[orderId-1] = request.json['quantity']
            order_delivery_address[orderId-1] = request.json['address']
            order_contact[orderId-1]= request.json['contact']
            
            return jsonify({'name':order_name[orderId-1],'id':order_id[orderId-1],'price':order_price[orderId-1],'quantity' : order_quantity[orderId-1],'address': order_delivery_address[orderId-1],'contact':order_contact[orderId-1]})
        
        except NameError:
            return jsonify({'status': 'failed!', 'message':'make a post request first'})
        except IndexError:
            return jsonify({'status': 'failed!', 'message':'No such order exists! Check the order ID'})

if __name__=='__main__':
    APP.run(debug=True)