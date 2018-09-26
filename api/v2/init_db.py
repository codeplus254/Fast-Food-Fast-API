"""THis python module conects to the database and creates the tables if they do not exist"""
import psycopg2
import os

hostname = os.getenv('HOSTNAME') 
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASENAME')


 
 
def create_tables():
    """ create tables in the PostgreSQL database"""
    

   
  
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            user_name VARCHAR(255) NOT NULL,
            user_password_hash VARCHAR(255) NOT NULL,
            user_type VARCHAR(5) NOT NULL
        )
        """,
        """ CREATE TABLE IF NOT EXISTS menu (
            
                meal_id SERIAL PRIMARY KEY,
                meal_name VARCHAR(50) NOT NULL,
                meal_price DECIMAL(6,2) NOT NULL,
                order_delivery_address VARCHAR(20) NOT NULL,
                order_quantity INTEGER NOT NULL,
                order_contact INTEGER NOT NULL
                )
        """,
        """ CREATE TABLE IF NOT EXISTS orders (
            
                order_id SERIAL PRIMARY KEY,
                meal_id INTEGER NOT NULL,
                order_price DECIMAL(6,2) NOT NULL,
                order_delivery_address VARCHAR(20) NOT NULL,
                order_quantity INTEGER NOT NULL,
                order_contact INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (meal_id) REFERENCES menu(meal_id)
                )
        """)
    conn = None
    try:
        # read the connection parameters
       
        # connect to the PostgreSQL server
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
 
 
if __name__ == '__main__':
    create_tables()