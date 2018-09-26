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

secret_key = os.getenv('SECRET_KEY') 

@APP.route('/api/v2/auth/signup', methods=['POST'])
def signup():
    user_name = request.json.get('username')
    user_password = request.json.get('password')
    user_token = jwt.encode({'user' : username, 
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=15)}, 
                secret_key)
    salt = "fast-food-fast"
    user = str(datetime.datetime.utcnow())+salt
    user_id = hashlib.md5(user.encode())
    
    
    #db.session.add(user)
    #db.session.commit()
    conn = None
    try:
        # read the connection parameters
       
        # connect to the PostgreSQL server
        conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )

        cur = conn.cursor()
        # create table one by one
        sql = """INSERT INTO TABLE_NAME (user_id, user_name, user_password_hash,user_type,user_token)
                VALUES (userid, value2, value3,...valueN);"""
        cur.execute("INSERT INTO users",(user_id,user_name,"hash","customer",user_token))
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return jsonify({ 'username': user_name, "token":user_token.decode('UTF-8'),"user_id":user_id.hexdigest()})

if __name__ == '__main__':
    APP.run(debug=True)

