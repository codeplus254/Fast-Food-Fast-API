import sys
sys.path.insert(0,'C:/Users/Ronny/fast-food-fast')
import psycopg2
import json
from flask import jsonify
import pytest 
import os
import ast
from api import create_app
secret_key = os.getenv('SECRET_KEY')
from flask import request, url_for
hostname = os.getenv('HOSTNAME') 
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
configuration = os.getenv('APP_SETTINGS')

APP2 = create_app(configuration)
tester = APP2.test_client()
database = os.getenv('DATABASENAME')

"""sign up user"""
"""testing the /api/v2/auth/signup POST request"""       
def test_signup():
    response = tester.post('/api/v2/auth/signup',
                                    content_type="application/json", data=json.dumps(
                                        {
                                            "email":"ronny@andela.com",
                                            "username": "ronny",
                                            "password":"password"
                                        })
                                        )
    assert "Sign Up successful" in json.loads(response.data)["Message"]
    assert response.status_code == 201
    global user_token
    text = response.get_data(as_text=True)
    user_token = ast.literal_eval(text.replace(" ", ""))['token']
    
 
def test_login():
    """testing the /api/v2/auth/login POST request"""
    response = tester.post('/api/v2/auth/login',
                                    content_type="application/json", data=json.dumps(
                                        {
                                            "email":"ronny@andela.com",
                                            "username": "ronny",
                                            "password":"password"
                                        })
                                        )
    assert "Login successful" in json.loads(response.data)["Message"]
    assert response.status_code == 200  
    global user_token
    text = response.get_data(as_text=True)
    user_token = ast.literal_eval(text.replace(" ", ""))['token'] 
         
 
               
def test_get_menu():
    """testing api/v2/menu GET request"""
    #unauthorized
    response = tester.get('/api/v2/menu')
    assert response.status_code == 401
    response = tester.get('/api/v2/menu',headers={'token': user_token}) 
    assert response.status_code == 200
def test_get_history_of_orders():
    """testing the /api/v2/orders GET request""" 
    response = tester.get('/api/v2/users/orders')
    assert response.status_code == 401
    response = tester.get('/api/v2/users/orders',headers={'token': user_token}) 
    assert response.status_code == 200
def test_get_specific_order():
    """Testing the .api/v2/orders/<orderId> GET request"""
    response = tester.get('/api/v2/orders/1')
    assert response.status_code == 401
    response = tester.get('/api/v2/orders/1',headers={'token': user_token}) 
    assert response.status_code == 401
def test_update_specific_order():
    """Testing the .api/v2/orders/<orderId> GET request"""
    response = tester.put('/api/v2/orders/1',
                                    content_type="application/json", data=json.dumps(
                                        {
                                          "order_status":"Processing"

                                        })
                                    )
    assert response.status_code == 401
    response = tester.put('/api/v2/orders/1',headers={'token': user_token},
                                    content_type="application/json", data=json.dumps(
                                        {
                                          "order_status":"Processing"

                                        })
                                    )
    assert response.status_code == 401

def test_logout():
    "Testing the api/v2/logout"
    response = tester.get('/api/v2/logout')
    assert response.status_code == 401
    response = tester.get('/api/v2/logout',headers={'token': user_token}) 
    assert response.status_code == 200

"""This test file is executed last hence the need for placing this last function of clearing db here"""
def test_clear_db():
    # connect to the PostgreSQL server
    conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    cur = conn.cursor()
    try:
        
        
        cur.execute("DROP TABLE orders, users, menu;")
        cur.close()
        conn.commit()
        conn.close()
   
    except (Exception, psycopg2.DatabaseError) as error:
        print(str(error))
    finally:
        if conn is not None:
            conn.close()


