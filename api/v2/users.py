import psycopg2
import hashlib
import os
import jwt
import datetime
from flask import jsonify

hostname = os.getenv('HOSTNAME') 
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASENAME')
salt = os.getenv('SALT')
secret_key = os.getenv('SECRET_KEY') 
user_token = None
user_id = None

class Users:
    def __init__(self,name,password,admin):
        self.name = name
        self.password = password
        passwd = self.password + salt
        self.passwd_hash = hashlib.md5(passwd.encode())
        self.admin = admin
        self.token = jwt.encode({'admin':admin,
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=15)}, 
                secret_key)
        
    def hash(self):
        sign_up_time = str(datetime.datetime.utcnow())+salt
        self.id = hashlib.md5(sign_up_time.encode())
        

    def signup(self):
        self.query_1 = """SELECT COUNT(*) FROM users WHERE user_name=%s;"""
        self.inputs_1 = (self.name,)
        self.query_2 = "INSERT INTO public.users (user_id, user_name, user_password_hash,user_type,user_token) VALUES (%s,%s,%s,%s,%s)"
        self.inputs_2 = (self.id.hexdigest(),self.name,self.passwd_hash.hexdigest(), 'admin',self.token)
        self.message = "Sign Up successful"
        self.error = "Sign up failed. Please choose another user name."
        self.event = "Signup"      
    
    def login(self):
        self.query = "SELECT user_id FROM users WHERE user_name=%s AND user_password_hash=%s"
        self.inputs = (self.name,self.passwd_hash.hexdigest())
        self.message = "Login successful"
        self.event = "Login" 
        self.error = "Login error"   
    def connect_db(self):
    
        conn = None
        self.status = 0
        
        try:
            # connect to the PostgreSQL server
            conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
           
            cur = conn.cursor()
            if self.event == "Signup":
                cur.execute(self.query_1,self.inputs_1)
                rows = cur.fetchone()
                #return jsonify({'user':rows[0]})
                if rows[0] == 0: #user does not exist
                    cur.execute(self.query_2,self.inputs_2)
                    # close communication with the PostgreSQL database server
                    cur.close()
                    # commit the changes
                    conn.commit()
                    print("User new")
                else: #user already exists      
                    self.status = 1         #throw error since user exists
                    print("User exists")
            else: #event is login
                       
                cur.execute(self.query,self.inputs)
                self.id = cur.fetchone()
                if self.id == None:     #user id does not exist
                    self.status=1
                    self.token = None
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.status = 1
            self.token = None
            self.error = "Database error: "+str(error)
        finally:
            if conn is not None:
                conn.close()
                
        