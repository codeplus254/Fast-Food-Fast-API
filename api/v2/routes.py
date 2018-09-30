"""This python module is responsible for creatinng user accounts and login"""
import sys
#sys.path.insert(0,'C:/Users/Ronny/fast-food-fast')
from flask import Flask, jsonify, request, make_response, Blueprint
from .users import Users
from .menu import Menu
from .orders import Orders
import jwt
import datetime
import os
import psycopg2
import hashlib

mod = Blueprint('v2', __name__)
hostname = os.getenv('HOSTNAME') 
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASENAME')
salt = os.getenv('SALT')
secret_key = os.getenv('SECRET_KEY') 
user_token = None
user_id = None
from functools import wraps


def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        #token = request.args.get('token')
        token = user_token
        if not token:
              return jsonify({'message': 'token is missing','token':token})
        try:
            admin = jwt.decode(token, secret_key) 
        except:
            return jsonify({'message': 'token is invalid'})
        return f(*args,**kwargs)
    return decorated
def admin_true(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        #token = request.args.get('token')
        token = user_token
        if not token:
              return jsonify({'message': 'token is missing','token':token})
        try:
            payload = jwt.decode(token, secret_key)
            if payload['admin'] == False:
                return jsonify({'message': 'You do not have clearance status to access this page'})
        except:
            return jsonify({'message': 'token is invalid'})
        return f(*args,**kwargs)
    return decorated





@mod.route('/users/orders', methods=['POST','GET'])
@token_required
def user_orders():
    if request.method == 'POST':  #a user can place an order
        meal_name = request.json.get('meal_name')
        order_delivery_address = request.json.get('order_address')
        order_quantity = request.json.get('order_quantity')
        order_contact = request.json.get('order_contact')
        order = Orders(user_id)
        order.place_order(meal_name,order_delivery_address,order_quantity,order_contact)
        order.connect_db()
        if order.status == 0:
            return jsonify({"Message": order.message})
        return jsonify({"Message": order.error,"Database Error": order.db_error })
    else:    #a user gets order history
        order = Orders(user_id)
        order.order_history()
        order.connect_db()
        if order.status == 0:
            return jsonify({"Message": order.message,"Orders":order.history})
        return jsonify({"Message": order.error,"Database Error": order.db_error })
@mod.route('/menu', methods=['GET'])
@token_required
def get_menu():
    menu = Menu()
    menu.get_menu()
    menu.connect_db()
    if menu.status == 0:
        return jsonify({"Message": menu.message,"menu":menu.MENU})
    return jsonify({"Message": menu.error,"Database Error": menu.db_error })
   

"""Test whether an admin can post a update menu """
@mod.route('/menu', methods=['POST'])
@token_required
@admin_true
def update_menu():
    meal_name = request.json.get('meal_name')
    meal_price = request.json.get('meal_price')
    menu = Menu()
    menu.update_menu(request.json.get('meal_name'), request.json.get('meal_price'))
    menu.connect_db()
    if menu.status == 0:
        return jsonify({"Message": menu.message})
    return jsonify({"Message": menu.error,"Database Error": menu.db_error })
    
@mod.route('/orders', methods=['GET'])
@token_required
@admin_true
def get_all_orders():

    conn = None
    try:
        conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )

        cur = conn.cursor()
        query = "SELECT * FROM public.orders "
            
            
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        # commit the changes
        conn.commit()
        conn.close()
        return jsonify({"message": "Fetched all orders."})
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({"message": "Failed to fetch all orders","Error":error})   

@mod.route('/auth/signup', methods=['POST'])
def signup():
    user_name = request.json.get('username')
    user_password = request.json.get('password')
    user_admin = request.json.get('admin')
    global user_token,user_id
    user = Users(request.json.get('username'), request.json.get('password'), request.json.get('admin'))
    user.hash()
    user.signup()
    user.connect_db()
    user_token = user.token
    user_id = user.id
    if user.status == 0:
        return jsonify({"message": user.message})
    return jsonify({"message": user.error})
    
@mod.route('/auth/login', methods=['POST'])
def login():
    #user_name = request.json.get('username')
    #user_password = request.json.get('password')
    #user_admin = request.json.get('admin')
    global user_token,user_id
    user = Users(request.json.get('username'), request.json.get('password'), request.json.get('admin'))
    user.login()
    user.connect_db()
    user_token = user.token
    user_id = user.id
    if user.status == 0:
        return jsonify({"message": user.message})
    return jsonify({"message": user.error})
        
if __name__ == '__main__':
    APP.run(debug=True)

