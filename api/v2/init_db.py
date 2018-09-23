import psycopg2
import os

hostname = os.getenv('HOSTNAME') 
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
print(password)
database = os.getenv('DATABASENAME')


 
 
def create_tables():
    """ create tables in the PostgreSQL database"""
    

   
  
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            user_name VARCHAR(255) NOT NULL,
            user_type VARCHAR(5) NOT NULL
        )
        """,
        """ CREATE TABLE IF NOT EXISTS orders (
            
                order_id INTEGER PRIMARY KEY,
                order_name VARCHAR(5) NOT NULL,
                order_price DECIMAL(6,2) NOT NULL,
                order_address VARCHAR(20) NOT NULL,
                order_contact INTEGER NOT NULL
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