import pytest
import psycopg2
import os
import sys
#sys.path.insert(0,'C:/Users/Ronny/fast-food-fast')
from api.v2 import init_db


hostname = os.getenv('HOSTNAME') 
assert hostname != None
username = os.getenv('USERNAME')
assert username != None
password = os.getenv('PASSWORD')
assert password != None
database = os.getenv('DATABASENAME')
assert database != None

def test_connect_to_database():
    conn = None
    
    # read the connection parameters
    
    # connect to the PostgreSQL server
    conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    assert conn != None
    
    
    conn.close()

