import sys
#sys.path.insert(0,'C:/Users/Ronny/fast-food-fast')
from api.v2.user_accounts import APP
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
    assert response.status_code == 200
"""testing the /api/v2/auth/login POST request""" 
def test_login():
    response = tester.post('/api/v2/auth/login',
                                    content_type="application/json", data=json.dumps(
                                        {
                                            "username": "ronny",
                                            "password":"password",
                                            "admin":1
                                        })
                                        ) 
    assert response.status_code == 200                              
"""testing the /api/v2/menu POST request"""       
def test_post_orders():
    response = tester.post('/api/v2/menu',
                                    content_type="application/json", data=json.dumps(
                                        {
                                            "meal_name":"samosa",
	                                        "meal_price":50.00
                                        })
                                    )
    
    
    assert response.status_code == 200
"""testing the /api/v2/orders GET request"""       
def test_get_all_orders():
    response = tester.get('/api/v2/orders')
    assert response.status_code == 200
    assert response.is_json == True
    
    