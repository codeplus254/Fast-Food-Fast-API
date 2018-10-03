import os
import psycopg2
from decimal import Decimal
hostname = os.getenv('HOSTNAME') 
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASENAME')
class Orders:
    def __init__(self,user_id):
        self.user_id = user_id
    def place_order(self,name,address,quantity,contact):
        """Place_order helps the user place an order"""
        self.name = name
        self.address = address
        self.quantity = quantity
        self.contact = contact
        self.event = "user_place_order"
        self.query_1 = "SELECT meal_price FROM menu WHERE meal_name=%s"
        self.input_1 = (self.name,)
        self.query_2 = """INSERT INTO public.orders (order_price,order_delivery_address,order_quantity,
                        order_contact,order_status,user_id, meal_name) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        self.message = "Order placed successfully."
        self.error = "Unable to place order. The meal is not available"
    def user_history(self):
        """Order_history helps the user see all his/her orders ever placed"""
        self.query_1 = "SELECT * FROM orders WHERE user_id=%s"
        self.input_1 = (self.user_id,) 
        self.event = "user_history"
        self.message = "Order history fetched successfully."
        self.error = "Unable to fetch order history."  
    def get_all_orders(self):
        """This function helps the admin see all orders placed"""
        self.query = "SELECT * FROM public.orders"
        self.message = "Successfully fetched all orders."
        self.error = "Unable to fetch all orders"
        self.event = "admin_get_all_orders"
    
    def get_specific_order(self,order_id):
        """This function enables the admin to fetch a specific order. Input is order_id"""
        self.query = "SELECT * FROM orders WHERE order_id=%s"
        self.input = (order_id,)     #tuple to support indexing
        self.query_1 = "SELECT order_id FROM orders ORDER BY order_id DESC LIMIT 1."
        self.event = "admin_get_specific_order"
        self.error = "Invalid order id"
        self.message = "Successfully fetched the order."
        self.order_id = order_id
        self.db_error = None
          
    def connect_db(self):
        self.status = 0
        conn = None
        try:
            conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
            cur = conn.cursor()
            if self.event == "user_place_order":
                #First let's get price for the meal from the MENU table
                
                cur.execute(self.query_1,self.input_1)
                meal_price = cur.fetchone()
                if meal_price is None:
                    self.status = 1
                
                self.price = Decimal(self.quantity) * meal_price[0]
                self.input_2 = (self.price, self.address, self.quantity,self.contact,"New",self.user_id,self.name)
                cur.execute(self.query_2,self.input_2)
            
                cur.close()
                conn.commit()
                conn.close()
            elif self.event == "user_history":
                cur.execute(self.query_1,self.input_1)
                self.orders = cur.fetchall()
                self.history = []
                for i in range(len(self.orders)):
                    self.history.append({'order_id':self.orders[i][0],
                                'order_price':str(self.orders[i][1]),    #Decimal type not JSON seriailzable
                                'order_delivery_address':self.orders[i][2],
                                'order_quantity':self.orders[i][3],
                                'order_contact' :self.orders[i][4],
                                'order_status' :self.orders[i][5],
                                'user_id' :self.orders[i][6],
                                'meal_name' :self.orders[i][7],
                                })
                cur.close()
                # commit the changes
                conn.commit()
                conn.close()
            elif self.event == "admin_get_all_orders":
                cur.execute(self.query)
                self.orders = cur.fetchall()
                self.ALL_ORDERS = []
                for i in range(len(self.orders)):
                    self.ALL_ORDERS.append({'order_id':self.orders[i][0],
                                'order_price':self.orders[i][1],
                                'order_delivery_address':self.orders[i][2],
                                'order_quantity':self.orders[i][3],
                                'order_contact':self.orders[i][4],
                                'order_status':self.orders[i][5],
                                'user_id':self.orders[i][6],
                                'meal_name':self.orders[i][7]
                                })
                cur.close()
                conn.close()
            elif self.event == "admin_get_specific_order":
                #first get number of orders
                cur.execute(self.query_1)
                number_of_orders = cur.fetchone()
                if self.order_id in range(1,number_of_orders[0]+1):
                    
                    cur.execute(self.query, self.input)
                    specific_order = cur.fetchone()
                    self.specific_order = {'order_id':specific_order[0],
                                    'order_price':str(specific_order[1]),    #Decimal type not JSON seriailzable
                                    'order_delivery_address':specific_order[2],
                                    'order_quantity':specific_order[3],
                                    'order_contact' :specific_order[4],
                                    'order_status' :specific_order[5],
                                    'user_id' :specific_order[6],
                                    'meal_name' :specific_order[7],
                                    }
                else: #Order_id does not exist
                    self.status = 1
                cur.close()
                conn.close()
        except (Exception, psycopg2.DatabaseError) as error:
            self.status = 1
            self.db_error = "Database error: "+str(error)
        finally:
            if conn is not None:
                conn.close()
"""       
def user_orders():
    if request.method == 'POST':  #a user can place an order
        meal_name = request.json.get('meal_name')
        order_delivery_address = request.json.get('order_address')
        order_quantity = request.json.get('order_quantity'),
        order_contact = request.json.get('order_contact'),
        conn = None
        try:
            conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )

            cur = conn.cursor()
            #First let's get price for the meal from the MENU table
            query_1 = "SELECT * FROM menu WHERE meal_name=%s"
            cur.execute(query_1,meal_name)
            meal_price = cur.fetchone()
            #order_price = int(order_quantity)*meal_price[0]
            query_2 = INSERT INTO public.orders (order_price,order_delivery_address,order_quantity,
                        #order_contact,order_status,user_id, meal_name) VALUES (%s,%s,%s,%s,%s,%s,%s)
                
            values = (500, order_delivery_address, order_quantity,order_contact,"New",user_id,meal_price)
                
            cur.execute(query_2,values)
            
            cur.close()
            conn.commit()
            conn.close()
            return jsonify({"message": "Order posted successfully."})
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return jsonify({"message": "Unable to place order"})"""