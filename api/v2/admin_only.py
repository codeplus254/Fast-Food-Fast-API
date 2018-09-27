"""This python module allows admin to access certain routes"""
import sys
sys.path.insert(0,'C:/Users/Ronny/fast-food-fast')
from flask import Flask, jsonify, request, make_response
import jwt
import os
import psycopg2
from api.v2.the_app import APP
from api.v2.user_accounts import user_token
from functools import wraps

hostname = os.getenv('HOSTNAME') 
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASENAME')
secret_key = os.getenv('SECRET_KEY')
#user_token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhZG1pbiI6InRydWUiLCJleHAiOjE1MzgwMzExNDN9.L5TRkzGpNLSQiEF4m7Ez5BFRA9LAoNjt1FXNYJRnPpY'
#adda  meal option
def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = user_token
        if not token:
              return jsonify({'message': 'token is missing'})
        try:
            admin = jwt.decode(token, secret_key) 
        except:
            return jsonify({'message': 'token is invalid'})
        return f(*args,**kwargs)
    return decorated
@APP.route('/api/v2/menu', methods=['POST'])
@token_required
def update_menu():
    return jsonify({"Message":"Hey admin"})
    """try:
        payload = jwt.decode(user_token, secret_key)
        return jsonify({"Admin": payload['admin']})
    except jwt.ExpiredSignatureError:
        return jsonify({"Error": "Signature expired. Please log in again."})
    except jwt.InvalidTokenError:
        return jsonify({"Error": "Invalid token. Please log in again."})"""
