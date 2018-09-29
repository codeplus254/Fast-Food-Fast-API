import psycopg2
import os

conn = psycopg2.connect(host="localhost",database="suppliers", user="postgres", password="postgres")

def connect():
    """Connect to postgre server"""
    conn=None
    try:
        conn=psycopg2.connect(db_name="test", port ="5432",user="admin-==========================`- `", password="secret")
        cur=conn.cursor()
        cur.execute('SELECT version()')
        db_version= cur.fetchone()
        print(db_version)
    except:
        print("Badooo")



