
CREATE USER tester WITH PASSWORD 'travis-test';


\c postgres

        
CREATE TABLE users (
    email VARCHAR(255) PRIMARY KEY ,
    user_id VARCHAR(255) UNIQUE,
    user_name VARCHAR(255) NOT NULL,
    user_password_hash VARCHAR(255) NOT NULL,
    user_type VARCHAR(15) NOT NULL,
    user_token VARCHAR(255)
);
CREATE TABLE menu (
            
                meal_id SERIAL UNIQUE,
                meal_name VARCHAR(50) PRIMARY KEY,
                meal_price DECIMAL(6,2) NOT NULL
                );
CREATE TABLE orders (
            
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
                );
GRANT ALL PRIVILEGES ON TABLE users TO tester;
GRANT ALL PRIVILEGES ON TABLE menu TO tester;
GRANT ALL PRIVILEGES ON TABLE orders TO tester;
--enable user tester to access curval and nextvar functions ie. in serial
GRANT USAGE ON SEQUENCE menu_meal_id_seq TO tester;
GRANT USAGE ON SEQUENCE orders_order_id_seq TO tester;