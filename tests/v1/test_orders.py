from api.v1 import *
import pytest 
def test_app(client):
    response = client.get('/api/v1/orders')
    assert response.status_code == 200


def test_specific_order(client):
    response = client.get('/api/v1/orders/1')
    assert response.status_code == 200




def test_invalid_order_id(client):
    response = client.get('api/v1/orders/300')
    assert b'Invalid! Please check your order id' in response.data
