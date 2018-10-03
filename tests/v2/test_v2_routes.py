import sys
#sys.path.insert(0,'C:/Users/Ronny/fast-food-fast')
from api import APP
import json
from flask import jsonify
import pytest 
import os
secret_key = os.getenv('SECRET_KEY')


from flask import request, url_for


tester = APP.test_client()
"""sign up user"""
"""testing the /api/v2/auth/signup POST request"""       
def test_signup():
    response = tester.post('/api/v2/auth/signup',
                                    content_type="application/json", data=json.dumps(
                                        {
                                            "username": "ronny",
                                            "password":"password",
                                            "admin": 1
                                        })
                                        )
    assert "Sign Up successful" in json.loads(response.data)["Message"]
    assert response.status_code == 200
 
def test_login():
    """testing the /api/v2/auth/login POST request"""
    response = tester.post('/api/v2/auth/login',
                                    content_type="application/json", data=json.dumps(
                                        {
                                            "username": "ronny",
                                            "password":"password",
                                            "admin":1
                                        })
                                        )
    assert "Login successful" in json.loads(response.data)["Message"]
    assert response.status_code == 200                              
      
def test_update_menu():
    """testing the /api/v2/menu POST request""" 
    response = tester.post('/api/v2/menu',
                                    content_type="application/json", data=json.dumps(
                                        {
                                          "meal_name":"Grilled Chicken",
                                           "meal_price":650.00

                                        })
                                    )
    
    assert "Menu update successful." in json.loads(response.data)["Message"]
    assert response.status_code == 200
     
def test_get_all_orders():
    """testing the /api/v2/orders GET request""" 
    response = tester.get('/api/v2/orders')
    assert response.status_code == 200
    assert response.is_json == True
    assert "Successfully fetched all orders." in json.loads(response.data)["Message"]
    
def test_get_specific_order():
    """Testing the .api/v2/orders/<orderId> GET request"""
    response = tester.get('/api/v2/orders/1')
    assert response.status_code == 200
    #assert "Successfully fetched the order." in json.loads(response.data)["Message"]

def test_update_specific_order():
    """Testing the .api/v2/orders/<orderId> GET request"""
    response = tester.put('/api/v2/orders/1',
                                    content_type="application/json", data=json.dumps(
                                        {
                                          "order_status":"Processing"

                                        })
                                    )
    assert response.status_code == 200
    #assert "Successfully updated the order." in json.loads(response.data)['Message']