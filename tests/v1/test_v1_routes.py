"""THis python module tests responses for api_v1.py file"""
import json
from api import create_app

APP = create_app('testing')
TESTER = APP.test_client()

def test_get_specific_order_before_posting():
    """testing the /api/v1/orders/<orderId> GET request before the post request is made"""
    response = TESTER.get('/api/v1/orders/1')
    assert "Make a post request first" in json.loads(response.data)["Message"]
    assert response.status_code == 200
    assert response.is_json is True
def test_update_specific_order_before_posting():
    """testing the /api/v1/orders/<orderId> GET request before the post request is made"""
    response = TESTER.get('/api/v1/orders/1')
    assert "Make a post request first" in json.loads(response.data)["Message"]
    assert response.status_code == 200
    assert response.is_json is True
def test_post_orders():
    """testing the /api/v1/orders POST request"""
    response = TESTER.post('/api/v1/orders',
                           content_type="application/json", data=json.dumps(
                               {
                                   "name": "Hamburger",
                                   "price": "100.00",
                                   "quantity": 1,
                                   "address" : "Andela",
                                   "contact" : "0720682290"}))
    assert 'You have successfully posted this order.' in json.loads(response.data)["Message"] 
    assert response.status_code == 200
def test_get_all_orders_after_posting():
    """testing the /api/v1/orders GET request for fetching all orders"""
    response = TESTER.get('/api/v1/orders')
    assert response.status_code == 200
    assert "You have successfully fetched all orders." in json.loads(response.data)["Message"]
def test_get_specific_order():
    """testing the /api/v1/orders/<orderId> GET request for specific order"""
    response = TESTER.get('/api/v1/orders/1')
    success_msg = "You have successfully fetched the order." 
    assert success_msg in json.loads(response.data)["Message"]
    assert response.status_code == 200
    assert response.is_json is True
    #inexistent order id
    response_2 = TESTER.get('/api/v1/orders/1000')
    error_msg = "No such order exists! Check the order ID"
    assert error_msg in json.loads(response_2.data)["Message"]
    assert response_2.status_code == 200

def test_put_specific_orders():
    """testing the /api/v1/orders/<orderId> PUT request for specific order"""
    response = TESTER.put('/api/v1/orders/1',
                          content_type="application/json", data=json.dumps(
                              {
                                  "status": "Complete"}))
    success_msg = "You have successfully updated the order."
    assert success_msg in json.loads(response.data)["Message"]
    assert response.status_code == 200
    #invalid status input
    response_2 = TESTER.put('/api/v1/orders/1',
                            content_type="application/json", data=json.dumps(
                                {
                                    "status": "Pending"}))
    error_msg = "Please input a valid order status"
    assert error_msg in json.loads(response_2.data)["Message"]
    assert response_2.status_code == 200
    #inexistent order_id
    response_3 = TESTER.put('/api/v1/orders/1000',
                            content_type="application/json", data=json.dumps(
                                {
                                    "status": "Complete"}))
    error_msg = "No such order exists! Check the order ID"
    assert error_msg in json.loads(response_3.data)["Message"]
    assert response_3.status_code == 200