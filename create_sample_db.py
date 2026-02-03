import sqlite3
import random
from datetime import datetime, timedelta

# Create sample database
conn = sqlite3.connect('sample_ecommerce.db')
cursor = conn.cursor()

# Create customers table
cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    signup_date DATE NOT NULL,
    country TEXT,
    lifetime_value DECIMAL(10, 2) DEFAULT 0
)
''')

# Create products table
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER DEFAULT 0
)
''')

# Create orders table
cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    order_date TIMESTAMP NOT NULL,
    status TEXT CHECK(status IN ('pending', 'shipped', 'delivered', 'cancelled')),
    total_amount DECIMAL(10, 2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
)
''')

# Create order_items table
cursor.execute('''
CREATE TABLE IF NOT EXISTS order_items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price_per_unit DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
''')

# Sample data - Customers
customers_data = [
    ('john.doe@email.com', 'John', 'Doe', '2024-01-15', 'USA', 1250.50),
    ('jane.smith@email.com', 'Jane', 'Smith', '2024-02-20', 'Canada', 890.25),
    ('bob.wilson@email.com', 'Bob', 'Wilson', '2024-03-10', 'UK', 2340.00),
    ('alice.brown@email.com', 'Alice', 'Brown', '2024-01-05', 'USA', 567.80),
    ('charlie.jones@email.com', 'Charlie', 'Jones', '2024-04-12', 'Australia', 1890.40),
]

cursor.executemany(
    'INSERT INTO customers (email, first_name, last_name, signup_date, country, lifetime_value) VALUES (?, ?, ?, ?, ?, ?)',
    customers_data
)

# Sample data - Products
products_data = [
    ('Laptop Pro 15"', 'Electronics', 1299.99, 50),
    ('Wireless Mouse', 'Electronics', 29.99, 200),
    ('USB-C Cable', 'Accessories', 12.99, 500),
    ('Desk Chair', 'Furniture', 199.99, 30),
    ('Monitor 27"', 'Electronics', 349.99, 75),
    ('Keyboard Mechanical', 'Electronics', 89.99, 120),
    ('Webcam HD', 'Electronics', 79.99, 80),
    ('Desk Lamp', 'Furniture', 45.99, 150),
]

cursor.executemany(
    'INSERT INTO products (product_name, category, price, stock_quantity) VALUES (?, ?, ?, ?)',
    products_data
)

# Sample data - Orders
orders_data = [
    (1, '2024-01-20 10:30:00', 'delivered', 1329.98),
    (1, '2024-03-15 14:20:00', 'delivered', 42.98),
    (2, '2024-02-25 09:15:00', 'delivered', 890.25),
    (3, '2024-03-20 16:45:00', 'shipped', 1649.97),
    (3, '2024-04-10 11:30:00', 'pending', 690.00),
    (4, '2024-01-18 13:00:00', 'delivered', 567.80),
    (5, '2024-04-15 10:00:00', 'delivered', 1890.40),
]

cursor.executemany(
    'INSERT INTO orders (customer_id, order_date, status, total_amount) VALUES (?, ?, ?, ?)',
    orders_data
)

# Sample data - Order Items
order_items_data = [
    (1, 1, 1, 1299.99),  # Order 1: Laptop
    (1, 2, 1, 29.99),    # Order 1: Mouse
    (2, 3, 1, 12.99),    # Order 2: USB Cable
    (2, 2, 1, 29.99),    # Order 2: Mouse
    (3, 5, 2, 349.99),   # Order 3: Monitor
    (3, 6, 1, 89.99),    # Order 3: Keyboard
    (3, 7, 1, 79.99),    # Order 3: Webcam
    (4, 1, 1, 1299.99),  # Order 4: Laptop
    (4, 5, 1, 349.99),   # Order 4: Monitor
    (5, 4, 2, 199.99),   # Order 5: Desk Chair
    (5, 1, 1, 1299.99),  # Order 5: Laptop
    (6, 3, 2, 12.99),    # Order 6: USB Cable
    (6, 8, 12, 45.99),   # Order 6: Desk Lamp
    (7, 6, 2, 89.99),    # Order 7: Keyboard
    (7, 1, 1, 1299.99),  # Order 7: Laptop
    (7, 7, 2, 79.99),    # Order 7: Webcam
]

cursor.executemany(
    'INSERT INTO order_items (order_id, product_id, quantity, price_per_unit) VALUES (?, ?, ?, ?)',
    order_items_data
)

conn.commit()
conn.close()

print("Sample e-commerce database created successfully: sample_ecommerce.db")
print("\nDatabase contains:")
print("- customers: Customer information")
print("- products: Product catalog")
print("- orders: Order records")
print("- order_items: Items in each order")
