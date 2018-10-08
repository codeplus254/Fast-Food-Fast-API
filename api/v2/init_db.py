"""THis python module conects to the database and creates the tables and sets an intial admin"""
import sys
import psycopg2
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,dir_path)

from models.users import Users
print(dir_path)
#from flask import Flask,jsonify, Blueprint

#APP_INIT = Flask(__name__)
hostname = os.getenv('HOSTNAME') 
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASENAME')
admin_name = os.getenv('ADMIN_NAME')
admin_password = os.getenv('ADMIN_PASSWORD')
admin_email = os.getenv('ADMIN_EMAIL')
 
 
def create_tables():
    """ create tables in the PostgreSQL database"""
    

   
  
    commands = (
        """CREATE SCHEMA IF NOT EXISTS public""",
        """
        CREATE TABLE IF NOT EXISTS users (
            email VARCHAR(255) PRIMARY KEY ,
            user_id VARCHAR(255) UNIQUE,
            user_name VARCHAR(255) NOT NULL,
            user_password_hash VARCHAR(255) NOT NULL,
            user_type VARCHAR(15) NOT NULL,
            user_token VARCHAR(255)
        )
        """,
        """ CREATE TABLE IF NOT EXISTS menu (
            
                meal_id SERIAL UNIQUE ,
                meal_name VARCHAR(50) PRIMARY KEY ,
                meal_price DECIMAL(6,2) NOT NULL
                )
        """,
        """ CREATE TABLE IF NOT EXISTS orders (
            
                order_id SERIAL PRIMARY KEY,
                order_price DECIMAL(6,2) NOT NULL,
                order_delivery_address VARCHAR(20) NOT NULL,
                order_quantity INTEGER NOT NULL,
                order_contact INTEGER NOT NULL,
                order_status VARCHAR(50) NOT NULL,
                user_id VARCHAR(255) NOT NULL,
                meal_name VARCHAR(50) NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (meal_name) REFERENCES menu(meal_name)
                )
        """)
    conn = None
    try:
        # connect to the PostgreSQL server
        #print(database)
        conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )

        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

#@APP_INIT.route('/api/v2/admin', methods=['POST'])
def create_admin():
    global user_token,user_id
    print(database)
    user = Users(admin_email,admin_name, admin_password, 1)
    user.hash()
    user.signup()
    user.connect_db()
    """user_token = user.token
    #user_id = user.id
    if user.status == 0:
        return jsonify({"Message": user.message,"token":user_token.decode("utf-8")}),201
    return jsonify({"Message": user.error}),403 """
 
if __name__ == "__main__":
    create_tables()
    #APP_INIT.run()
    create_admin()