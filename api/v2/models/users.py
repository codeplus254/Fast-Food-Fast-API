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
    def __init__(self,email,name,password,admin):
        self.email = email
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
        self.query_1 = "SELECT COUNT(user_name) FROM users WHERE email=%s;"
        self.inputs_1 = (self.email,)
        self.query_2 = "INSERT INTO public.users (email,user_id, user_name, user_password_hash,user_type,user_token) VALUES (%s,%s,%s,%s,%s,%s)"
        self.inputs_2 = (self.email, self.id.hexdigest(),self.name,self.passwd_hash.hexdigest(), str(self.admin),self.token.decode("utf-8"))
        self.message = "Sign Up successful"
        self.error = "Sign up failed. This email is already registered.."
        self.event = "Signup"      
    
    def login(self):
        self.query_1 = "SELECT user_id FROM users WHERE email=%s AND user_password_hash=%s;"
        self.inputs_1 = (self.email, self.passwd_hash.hexdigest())
        self.query_2 = "UPDATE users SET user_token=%s WHERE user_name=%s AND email=%s"
        self.inputs_2 = (self.token.decode("utf-8"),self.name,self.email)
        self.message = "Login successful"
        self.event = "Login" 
        self.error = "Login failed. Check you credentials again!" 
    def logout(self):
        self.query_1 = "UPDATE users SET user_token=%s WHERE user_name=%s AND email=%s" 
        self.inputs_1 = (None,self.name,self.email)
        self.message = "Logout successful"
        self.event = "Logout" 
        self.error = "Log out failed!"
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
                    cur.close()
                    conn.commit()
                    
                else: #user already exists      
                    self.status = 1         #throw error since user exists
                    
            elif self.event == "Login":
                       
                cur.execute(self.query_1,self.inputs_1)                 #get user id
                self.id = cur.fetchone()
                cur.execute(self.query_2,self.inputs_2)
                conn.commit()
                if self.id == None:     #user id does not exist
                    self.status=1
                    self.token = None
            else: #event is log out
                cur.execute(self.query_1,self.inputs_1)
                conn.commit()
                
                self.token = None
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.status = 1
            self.token = None
            self.error = "Database error: "+str(error)
        finally:
            if conn is not None:
                conn.close()
                
        