import os
import psycopg2
hostname = os.getenv('HOSTNAME') 
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASENAME')
class Menu:
    def get_menu(self):
        self.event = "fetch"
        self.message = "Here's the menu."
        self.error = "Failed to get the menu"
        self.query = "SELECT * FROM public.menu "
    def update_menu(self,name,price):
        self.name = name
        self.price = price
        self.event = "update"
        self.message = "Menu update successful."
        self.error = "Menu update not successful. The meal name already exists!"
        self.query_1 = "SELECT COUNT(*) FROM menu WHERE meal_name=%s;"
        self.input_1 = (self.name,)
        self.query_2 = "INSERT INTO public.menu (meal_name, meal_price) VALUES (%s,%s)"
        self.input_2 = (self.name,self.price)

    def connect_db(self):
        conn = None
        self.status = 0
        self.db_error = None
        try:
            conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )

            cur = conn.cursor()
            #first check if the meal name exists
            if self.event == "update":
                print("firing up update")
                cur.execute(self.query_1,self.input_1)
                rows = cur.fetchone()
                print("first fetch done")
                print('user: '+str(rows[0]))
                if rows[0] == 0: #meal name does not exist in  menu
                    print('in if statement')
                    cur.execute(self.query_2,self.input_2)
                    print("updated menu")
                    # close communication with the PostgreSQL database server
                    cur.close()
                    # commit the changes
                    conn.commit()
                else: #meal name already exists      
                    self.status = 1         #throw error since user exists
                print("finally updated menu")    
            else: #user fetches menu
                cur.execute(self.query)
                self.meals = cur.fetchall()
                self.MENU = []
                for i in range(len(self.meals)):
                    self.MENU.append({'meal_id':self.meals[i][0],
                                'meal_name':self.meals[i][1],
                                'meal_price':str(self.meals[i][2])     #Decimal type not JSON seriailzable
                                })
                cur.close()
                # commit the changes
                conn.commit()
                conn.close()


        except (Exception, psycopg2.DatabaseError) as error:
            self.status = 1
            self.db_error = "Database error: "+str(error)
        finally:
            if conn is not None:
                conn.close()
