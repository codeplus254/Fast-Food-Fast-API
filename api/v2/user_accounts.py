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

@APP.route('/api/v2/auth/signup', methods=['POST'])
def signup():
    user_name = request.json.get('username')
    user_password = request.json.get('password')
    user_token = jwt.encode({'admin':True,
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=15)}, 
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
    user_token = jwt.encode({'admin':True,
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
    if isinstance(user_id,tuple) == False:
        return jsonify({"Error":"Login failed", "message": "Please sign up"})
    #else
    return jsonify({"message": "Login successful"})
if __name__ == '__main__':
    APP.run(debug=True)

