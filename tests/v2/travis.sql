
CREATE USER tester WITH PASSWORD 'travis-test';


CREATE DATABASE test_fast_food_fast;
\c test_fast-food_fast
GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP ON DATABASE test_fast_food_fast TO tester;
CREATE SCHEMA IF NOT EXISTS public;
        
CREATE TABLE IF NOT EXISTS users (
    email VARCHAR(255) PRIMARY KEY ,
    user_id VARCHAR(255) UNIQUE,
    user_name VARCHAR(255) NOT NULL,
    user_password_hash VARCHAR(255) NOT NULL,
    user_type VARCHAR(15) NOT NULL,
    user_token VARCHAR(255)
)
 CREATE TABLE IF NOT EXISTS menu (
            
                meal_id SERIAL UNIQUE ,
                meal_name VARCHAR(50) PRIMARY KEY ,
                meal_price DECIMAL(6,2) NOT NULL
                )
CREATE TABLE IF NOT EXISTS orders (
            
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


