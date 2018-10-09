"""This python module is responsible for creatinng user accounts and login"""
#import sys
#sys.path.insert(0,r'C:\Users\Ronny\fast-food-fast')
from flask import Flask, jsonify, request, make_response, Blueprint
import jwt
import datetime
import os
import psycopg2
import hashlib
import re
from .models.users import Users
from .models.menu import Menu
from .models.orders import Orders


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
        
        if 'Token' in request.headers:
            token = request.headers['Token']
            """Let's make sure the current user is using his/her token"""
            try:
                # connect to the PostgreSQL server
                conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
            
                cur = conn.cursor()
                query = "SELECT user_token FROM users WHERE user_id=%s;"
                inputs=(user_id,)
                
                cur.execute(query,inputs)
                db_token = cur.fetchone()[0]
                if db_token == token:
                    try:
                        admin = jwt.decode(token, secret_key) 
                        
                    except:
                        return jsonify({'Message': 'token is invalid'}),403
                    return f(*args,**kwargs)
                else:
                    return jsonify({"Message":"Use your own token"}),403
                cur.close()
                conn.close()
            except (Exception, psycopg2.DatabaseError) as error:
            
                return jsonify({"Database error":str(error)})
            finally:
                if conn is not None:
                    conn.close()
        else:
            return jsonify({'message': 'token is missing in header'}), 401
    return decorated
def admin_true(f):
    @wraps(f)
    def decorated(*args,**kwargs):
         #token = request.args.get('token')
        if 'Token' in request.headers:
            token = request.headers['token']
            if not token:
                return jsonify({'message': 'token is missing','token':token}),403
            try:
                payload = jwt.decode(token, secret_key)
                if payload['admin'] == False:
                    return jsonify({'message': 'You do not have clearance status to access this page'}),401
            except:
                return jsonify({'message': 'token is invalid'}),403
            return f(*args,**kwargs)
        else:
            return jsonify({'message': 'token is missing in header'}), 401
    return decorated

def validate_password(passwd):
    valid = True
    while valid:  
        if (len(passwd)<8 or len(passwd)>20):
            break
        elif not re.search("[a-z]",passwd):
            break
        elif not re.search("[0-9]",passwd):
            break
        elif not re.search("[A-Z]",passwd):
            break
        elif re.search("\s",passwd): #ensure no spaces,tabs or blanks
            break
        else:
            valid=False
            break

    if valid==False:
        return jsonify({'Message': 'Password should contain at least one uppercase letter,lowercase letter,one number and no spaces.'}), 403
def validate_email(email):
    EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

    if not EMAIL_REGEX.match(email):
        return jsonify({'Message': 'Please enter a proper email address.'}), 403


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
            return jsonify({"Message": order.message}),201
        
        return jsonify({"Message": order.error,"Database Error": order.db_error }),403
    else:    #a user gets order history
        order = Orders(user_id)
        order.user_history()
        order.connect_db()
        if order.status == 0:
            return jsonify({"Message": order.message,"Orders":order.history}),200
        return jsonify({"Message": order.error,"Database Error": order.db_error }),404
@mod.route('/menu', methods=['GET'])
@token_required
def get_menu():
    menu = Menu()
    menu.get_menu()
    menu.connect_db()
    if menu.status == 0:
        return jsonify({"Message": menu.message,"menu":menu.MENU}),200
    return jsonify({"Message": menu.error,"Database Error": menu.db_error }),404
   

"""Test whether an admin can update menu """
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
        return jsonify({"Message": menu.message}),201
    else:
        if menu.db_error is not None:           #database error present
            return jsonify({"Database Error": menu.db_error }),500
        return jsonify({"Message": menu.error}),304
@mod.route('/orders', methods=['GET'])
@token_required
@admin_true
def get_all_orders():
    orders = Orders(user_id)
    orders.get_all_orders()
    orders.connect_db()
    if orders.status == 0:
        return jsonify({"Message": orders.message,"Orders":orders.ALL_ORDERS}),200
    else:
        if orders.db_error is not None:           #database error present
            return jsonify({"Database Error": orders.db_error }),500
        return jsonify({"Message": orders.error}),404
@mod.route('/orders/<int:specific_order_id>', methods=['GET','PUT'])
@token_required
@admin_true
def specific_order(specific_order_id):
    if request.method == 'GET':
        order = Orders(user_id)
        order.get_specific_order(specific_order_id)
        order.connect_db()
        if order.status == 0:
            return jsonify({"Message": order.message,"Order":order.specific_order}),200
        else:
            if order.db_error is not None:           #database error present
                return jsonify({"Database Error": order.db_error }),500
            return jsonify({"Message": order.error}),404  
    else: #PUT request
        status = request.json.get('order_status')
        order = Orders(user_id)
        order.update_specific_order(status,specific_order_id)
        order.connect_db()
        if order.status == 0:
            return jsonify({"Message": order.message,"Order":order.specific_order}),200
        else:
            if order.db_error is not None:           #database error present
                return jsonify({"Database Error": order.db_error }),500
            return jsonify({"Message": order.error}),304
@mod.route('/logout', methods=['GET'])
@token_required
def logout():
    user = Users(email, user_name, user_password,0)
    user.logout()
    user.connect_db()
    return jsonify({"Message":user.message})

@mod.route('/auth/signup', methods=['POST'])
def signup():
    global user_id,email,user_name,user_password
    email = request.json.get('email')
    user_name = request.json.get('username')
    user_password = request.json.get('password')
    user_admin = 0
    
    user = Users(email, user_name, user_password,0)
    user.hash()
    user.signup()
    user.connect_db()
    user_token = user.token
    if user.status == 0:
        user_id = user.id.hexdigest()
        return jsonify({"Message": user.message,"token":user_token.decode("utf-8")}),201
    return jsonify({"Message": user.error}),403    
@mod.route('/auth/login', methods=['POST'])
def login():
    global user_id,email,user_name,user_password
    email = request.json.get('email')
    user_name = request.json.get('username')
    user_password = request.json.get('password')
    user_admin = 0
    #validate_password(user_password)
    #validate_email(email)
    user = Users(email, user_name, user_password,0)
    user.login()
    
    user.connect_db()
    user_token = user.token
    if user.status == 0:
        user_id = user.id
        return jsonify({"Message": user.message,"token":user_token.decode("utf-8")}),200
    return jsonify({"Message": user.error}),403
    
@mod.route('/admin/login', methods=['POST'])
def admin_login():
    global user_id,email,user_name,user_password
    email = request.json.get('email')
    user_name = request.json.get('username')
    user_password = request.json.get('password')
    #user_admin = 1
    user = Users(email, user_name, user_password,1)
    user.login()
    user.connect_db()
    user_token = user.token
    
    if user.status == 0:
        user_id = user.id
        return jsonify({"Message": user.message,"token":user_token.decode("utf-8")}),200
    return jsonify({"Message": user.error}),403
@mod.route('/admin/signup', methods=['POST'])
@token_required
@admin_true
def admin_signup_others():
    global user_id,email,user_name,user_password
    email = request.json.get('email')
    user_name = request.json.get('username')
    user_password = request.json.get('password')
    user_admin = request.json.get('admin')
    #validate_password(user_password)
    #validate_email(email)
    user = Users(email, user_name, user_password,user_admin)
    user.hash()
    #user.admin_token() #overrides the user token given above
    user.signup()
    user.connect_db()
    if user.status == 0:
        user_id2 = user.id.hexdigest()[0]
        return jsonify({"Message": user.message}),201
    return jsonify({"Message": user.error}),401
        
if __name__ == '__main__':
    APP.run(debug=True)

