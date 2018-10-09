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

APP = create_app(configuration)
tester = APP.test_client()
#after environment variable has been set
database = os.getenv('DATABASENAME')

        

    


def test_login():
    """testing the /api/v2/admin/login POST request"""
    response = tester.post('/api/v2/admin/login',
                                    content_type="application/json", data=json.dumps(
                                        {
                                            "email":"admin@andela.com",
                                            "username": "admin",
                                            "password":"Andela1"
                                        })
                                        )
    assert "Login successful" in json.loads(response.data)["Message"]
    assert response.status_code == 200  
    global user_token
    text = response.get_data(as_text=True)
    user_token = ast.literal_eval(text.replace(" ", ""))['token'] 
"""sign up user"""
"""testing the /api/v2/auth/signup POST request"""       
def test_signup_other_admins():
    response = tester.post('/api/v2/admin/signup',
                                    content_type="application/json", data=json.dumps(
                                        {
                                            "email":"admin2@andela.com",
                                            "username": "admin_2",
                                            "password":"Andela2"
                                        })
                                        )
    assert response.status_code == 401
    response = tester.post('/api/v2/admin/signup',headers={'token': user_token},
                                    content_type="application/json", data=json.dumps(
                                        {
                                            "email":"admin2@andela.com",
                                            "username": "admin_2",
                                            "password":"Andela2"
                                        })
                                        )
    assert "Sign Up successful" in json.loads(response.data)["Message"]
    assert response.status_code == 201
    
def test_update_menu():
    """testing adding food to menu"""
    response = tester.post('/api/v2/menu',
                                    content_type="application/json", data=json.dumps(
                                        {
                                            "meal_name":"pizza",
                                            "meal_price":700.00
                                        })
                                        )
    assert response.status_code == 401
    response = tester.post('/api/v2/menu',headers={'token': user_token},
                                    content_type="application/json", data=json.dumps(
                                        {
                                            "meal_name":"pizza",
                                            "meal_price":700.00
                                        })
                                        )
    assert "Menu update successful" in json.loads(response.data)["Message"]
    assert response.status_code == 201
def test_get_menu():
    """testing api/v2/menu GET request"""
    #unauthorized
    response = tester.get('/api/v2/menu')
    assert response.status_code == 401
    response = tester.get('/api/v2/menu',headers={'token': user_token}) 
    assert response.status_code == 200 
def test_place_order():
    """testing api/v2/users/orders"""
    response = tester.post('/api/v2/users/orders',
                                    content_type="application/json", data=json.dumps(
                                        {
                                            "meal_name":"pizza",
                                            "order_address" : "Andela",
                                            "order_quantity" : "2",
                                            "order_contact" : 720682290
                                        })
                                        )
    assert response.status_code == 401
    response = tester.post('/api/v2/users/orders',headers={'token': user_token},
                                    content_type="application/json", data=json.dumps(
                                        {
                                            "meal_name":"pizza",
                                            "order_address" : "Andela",
                                            "order_quantity" : "2",
                                            "order_contact" : 720682290
                                        })
                                        )
    #assert "Order placed successfully" in json.loads(response.data)['Message']
    assert response.status_code == 201

               

def test_get_history_of_orders():
    """testing the /api/v2/orders GET request""" 
    response = tester.get('/api/v2/orders')
    assert response.status_code == 401
    response = tester.get('/api/v2/orders',headers={'token': user_token}) 
    assert response.status_code == 200
def test_get_specific_order():
    """Testing the .api/v2/orders/<orderId> GET request"""
    response = tester.get('/api/v2/orders/1')
    assert response.status_code == 401
    response = tester.get('/api/v2/orders/1',headers={'token': user_token}) 
    assert response.status_code == 200
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
    assert response.status_code == 200


    