"""This python module is responsible for creatinng user accounts and login"""
import sys
sys.path.insert(0,'C:/Users/Ronny/fast-food-fast')
from flask import Flask, jsonify, request, make_response
import jwt
from api.v2.the_app import APP
import datetime
import os
import psycopg2
import hashlib

hostname = os.getenv('HOSTNAME') 
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASENAME')
salt = os.getenv('SALT')
secret_key = os.getenv('SECRET_KEY') 
user_token = None
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
@APP.route('/api/v2/menu', methods=['POST'])
@token_required
@admin_true
def update_menu():
    meal_name = request.json.get('meal_name')
    meal_price = request.json.get('meal_price')

    conn = None
    try:
        conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )

        cur = conn.cursor()
        query = "INSERT INTO public.menu (meal_name, meal_price) VALUES (%s,%s)"
            
        values = (meal_name,meal_price)
            
        cur.execute(query,values)
        
        cur.close()
        # commit the changes
        conn.commit()
        conn.close()
        return jsonify({"message": "Menu update successful."})
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({"message": "Menu update not successful.","Error":error})
@APP.route('/api/v2/orders', methods=['GET'])
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

@APP.route('/api/v2/auth/signup', methods=['POST'])
def signup():
    user_name = request.json.get('username')
    user_password = request.json.get('password')
    user_admin = request.json.get('admin')
    global user_token
    user_token = jwt.encode({'admin':user_admin,
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=15)}, 
                secret_key)
    
    user = str(datetime.datetime.utcnow())+salt
    user_id = hashlib.md5(user.encode())
    passwd = user_password + salt
    user_passwd_hash = hashlib.md5(passwd.encode())
    
    #db.session.add(user)
    #db.session.commit()
    conn = None
    status = 0
    try:
        # read the connection parameters
       
        # connect to the PostgreSQL server
        conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
        
        cur = conn.cursor()
        # create table one by one
        query_1 = "SELECT COUNT(*) FROM users WHERE user_name=%s AND user_password_hash=%s"
        inputs = (user_name,user_passwd_hash.hexdigest())
        
        cur.execute(query_1,inputs)
        rows = cur.fetchone()
        #return jsonify({'user':rows})
        if rows[0] == 0:
            query = "INSERT INTO public.users (user_id, user_name, user_password_hash,user_type,user_token) VALUES (%s,%s,%s,%s,%s)"
            
            values = (user_id.hexdigest(),user_name,user_passwd_hash.hexdigest(), 'admin',user_token)
            
            cur.execute(query,values)
            # close communication with the PostgreSQL database server
            cur.close()
            # commit the changes
            conn.commit()
            
        else:
            cur.close()
            status = 1
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    if status == 0:
        return jsonify({"message": "Sign Up successful"})
    return jsonify({ "Error":"Sign UP failed", "message": "Please choose another user name"})
@APP.route('/api/v2/auth/login', methods=['POST'])
def login():
    user_name = request.json.get('username')
    user_password = request.json.get('password')
    user_admin = request.json.get('admin')
    global user_token
    user_token = jwt.encode({'admin':user_admin,
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=15)}, 
                secret_key)
    
    user = str(datetime.datetime.utcnow())+salt
    user_id = hashlib.md5(user.encode())
    passwd = user_password + salt
    user_passwd_hash = hashlib.md5(passwd.encode())
    
    conn = None
    try:
        conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )

        cur = conn.cursor()
        query = "SELECT user_id FROM users WHERE user_name=%s AND user_password_hash=%s"
        values = (user_name,user_passwd_hash.hexdigest())
        
        cur.execute(query,values)
        user_id = cur.fetchone()
        

        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    #else
    return jsonify({"message": "Login successful", "token":user_token.decode('UTF-8')})

if __name__ == '__main__':
    APP.run(debug=True)

