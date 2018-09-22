import sys
sys.path.insert(0,'C:/Users/Ronny/fast-food-fast')
from api.v1.api_v1 import APP
import json

import pytest 



from flask import request, url_for


tester = APP.test_client()

def test_index():
        
        response = tester.get('/')
        print(response.status_code)
        assert b'Fast Food Fast API' in response.data
        assert response.status_code == 200
"""testing the /api/v1/orders GET request"""       
def test_get_all_orders():
    response = tester.get('/api/v1/orders')
    assert response.status_code == 200
    assert response.is_json == True
    
"""testing the /api/v1/orders GET request"""       
def test_post_orders():
    response = tester.post('/api/v1/orders',
                                    content_type="application/json", data=json.dumps(
                                        {
                                            "id": 1,
                                            "name": "fries",
                                            "price": "100.00",
                                            "quantity": 1,
                                            "address" : "Andela",
                                            "contact" : "0720682290"
                                        })
                                    )
    assert b'{"address":["Andela"],"contact":["0720682290"],"id":[1],"name":["fries"],"price":["100.00"],"quantity":[1]}' in response.data
    assert response.status_code == 200   


def test_get_specific_order():
    response = tester.get('/api/v1/orders/1')
    assert response.status_code == 200
    assert b'{"address":"Andela","contact":"0720682290","id":1,"name":"fries","price":"100.00","quantity":1}' in response.data
   
    assert response.is_json == True

def test_put_specific_orders():
    response = tester.put('/api/v1/orders/1',
                                    content_type="application/json", data=json.dumps(
                                        {
                                            "name": "fries",
                                            "price": "100.00",
                                            "quantity": 2,
                                            "address" : "Westlands",
                                            "contact" : "0720682290"
                                        })
                                    )
    print(response.data)
    assert b'{"address":"Westlands","contact":"0720682290","id":1,"name":"fries","price":"100.00","quantity":2}' in response.data
   
    assert response.status_code == 200