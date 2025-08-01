"""Script to create and populate a sample SQLite database for testing the chatbot."""

import sqlite3
from datetime import datetime, timedelta
import random

def create_sample_database():
    """Create a sample database with realistic test data."""
    
    # Connect to database (creates file if it doesn't exist)
    conn = sqlite3.connect('sample_database.db')
    cursor = conn.cursor()
    
    # Create tables
    create_tables(cursor)
    
    # Populate with sample data
    populate_customers(cursor)
    populate_products(cursor)
    populate_orders(cursor)
    populate_order_items(cursor)
    populate_employees(cursor)
    
    # Commit changes and close
    conn.commit()
    conn.close()
    
    print("Sample database created successfully!")
    print("Database file: sample_database.db")
    print("\nTables created:")
    print("- customers (100 records)")
    print("- products (50 records)")
    print("- orders (200 records)")
    print("- order_items (500+ records)")
    print("- employees (20 records)")

def create_tables(cursor):
    """Create all database tables."""
    
    # Customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            registration_date DATE,
            total_spent DECIMAL(10,2) DEFAULT 0.00
        )
    ''')
    
    # Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            stock_quantity INTEGER DEFAULT 0,
            description TEXT,
            supplier TEXT,
            created_date DATE
        )
    ''')
    
    # Orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            order_date DATE NOT NULL,
            total_amount DECIMAL(10,2) NOT NULL,
            status TEXT DEFAULT 'pending',
            shipping_address TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        )
    ''')
    
    # Order items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER NOT NULL,
            unit_price DECIMAL(10,2) NOT NULL,
            total_price DECIMAL(10,2) NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (order_id),
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        )
    ''')
    
    # Employees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT,
            position TEXT,
            salary DECIMAL(10,2),
            hire_date DATE,
            manager_id INTEGER,
            FOREIGN KEY (manager_id) REFERENCES employees (employee_id)
        )
    ''')

def populate_customers(cursor):
    """Populate customers table with sample data."""
    
    first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Lisa', 'Robert', 'Emily', 'James', 'Jessica',
                   'William', 'Ashley', 'Richard', 'Amanda', 'Joseph', 'Stephanie', 'Thomas', 'Nicole', 'Christopher', 'Elizabeth']
    
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
                  'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']
    
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
    states = ['NY', 'CA', 'IL', 'TX', 'AZ', 'PA', 'TX', 'CA', 'TX', 'CA']
    
    customers_data = []
    for i in range(100):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        email = f"{first_name.lower()}.{last_name.lower()}{i}@email.com"
        phone = f"({random.randint(200,999)}) {random.randint(200,999)}-{random.randint(1000,9999)}"
        address = f"{random.randint(100,9999)} {random.choice(['Main', 'Oak', 'Pine', 'Elm', 'Cedar'])} St"
        city_idx = random.randint(0, len(cities)-1)
        city = cities[city_idx]
        state = states[city_idx]
        zip_code = f"{random.randint(10000,99999)}"
        reg_date = datetime.now() - timedelta(days=random.randint(30, 1000))
        total_spent = round(random.uniform(50, 5000), 2)
        
        customers_data.append((first_name, last_name, email, phone, address, city, state, zip_code, reg_date.date(), total_spent))
    
    cursor.executemany('''
        INSERT INTO customers (first_name, last_name, email, phone, address, city, state, zip_code, registration_date, total_spent)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', customers_data)

def populate_products(cursor):
    """Populate products table with sample data."""
    
    products_data = [
        ('Laptop Pro 15"', 'Electronics', 1299.99, 25, 'High-performance laptop with 16GB RAM', 'TechCorp', '2024-01-15'),
        ('Wireless Mouse', 'Electronics', 29.99, 150, 'Ergonomic wireless mouse with USB receiver', 'TechCorp', '2024-01-20'),
        ('Office Chair', 'Furniture', 199.99, 40, 'Ergonomic office chair with lumbar support', 'ComfortSeating', '2024-02-01'),
        ('Standing Desk', 'Furniture', 399.99, 15, 'Adjustable height standing desk', 'DeskMakers', '2024-02-05'),
        ('Coffee Maker', 'Appliances', 89.99, 60, 'Programmable coffee maker with timer', 'BrewMaster', '2024-01-10'),
        ('Smartphone X', 'Electronics', 799.99, 80, 'Latest smartphone with advanced camera', 'PhoneTech', '2024-01-25'),
        ('Bluetooth Headphones', 'Electronics', 149.99, 100, 'Noise-canceling wireless headphones', 'AudioPro', '2024-02-10'),
        ('Desk Lamp', 'Furniture', 45.99, 75, 'LED desk lamp with adjustable brightness', 'LightCorp', '2024-01-30'),
        ('External Hard Drive', 'Electronics', 79.99, 90, '1TB external storage device', 'DataStore', '2024-02-15'),
        ('Mechanical Keyboard', 'Electronics', 129.99, 50, 'RGB mechanical gaming keyboard', 'GameGear', '2024-01-05'),
        ('Monitor 24"', 'Electronics', 249.99, 35, '4K resolution computer monitor', 'DisplayTech', '2024-01-12'),
        ('Webcam HD', 'Electronics', 69.99, 120, '1080p HD webcam for video calls', 'CamTech', '2024-02-20'),
        ('Printer All-in-One', 'Electronics', 179.99, 30, 'Wireless printer with scanner and copier', 'PrintPro', '2024-01-18'),
        ('Tablet 10"', 'Electronics', 329.99, 45, 'Lightweight tablet with stylus support', 'TabletCorp', '2024-02-08'),
        ('Smart Watch', 'Electronics', 199.99, 70, 'Fitness tracking smartwatch', 'WearTech', '2024-01-22'),
        ('Bookshelf', 'Furniture', 129.99, 25, '5-tier wooden bookshelf', 'WoodCraft', '2024-02-12'),
        ('Table Lamp', 'Furniture', 34.99, 85, 'Modern table lamp with fabric shade', 'LightDesign', '2024-01-28'),
        ('Microwave Oven', 'Appliances', 119.99, 40, 'Compact microwave with digital controls', 'KitchenPro', '2024-02-03'),
        ('Blender', 'Appliances', 59.99, 55, 'High-speed blender for smoothies', 'BlendMaster', '2024-01-14'),
        ('Air Fryer', 'Appliances', 99.99, 65, 'Digital air fryer with multiple presets', 'CookSmart', '2024-02-18'),
        ('Gaming Mouse', 'Electronics', 79.99, 95, 'High-precision gaming mouse with RGB', 'GameGear', '2024-01-08'),
        ('USB Hub', 'Electronics', 24.99, 200, '7-port USB 3.0 hub', 'ConnectTech', '2024-02-25'),
        ('Desk Organizer', 'Office', 19.99, 150, 'Bamboo desk organizer with compartments', 'OrganizePro', '2024-01-16'),
        ('Whiteboard', 'Office', 49.99, 30, 'Magnetic dry erase whiteboard', 'BoardTech', '2024-02-07'),
        ('Shredder', 'Office', 89.99, 20, 'Cross-cut paper shredder', 'SecureShred', '2024-01-26'),
        ('File Cabinet', 'Furniture', 159.99, 18, '3-drawer locking file cabinet', 'OfficeFurn', '2024-02-14'),
        ('Ergonomic Cushion', 'Furniture', 29.99, 100, 'Memory foam seat cushion', 'ComfortPlus', '2024-01-11'),
        ('Power Strip', 'Electronics', 19.99, 180, '6-outlet surge protector power strip', 'PowerSafe', '2024-02-21'),
        ('Cable Management', 'Office', 14.99, 250, 'Under-desk cable management tray', 'CableClean', '2024-01-19'),
        ('Desk Pad', 'Office', 24.99, 120, 'Large leather desk pad', 'DeskStyle', '2024-02-09'),
        ('Monitor Stand', 'Furniture', 39.99, 80, 'Adjustable monitor stand with storage', 'DisplayRise', '2024-01-23'),
        ('Laptop Stand', 'Furniture', 49.99, 60, 'Aluminum laptop stand with cooling', 'LaptopLift', '2024-02-16'),
        ('Wireless Charger', 'Electronics', 34.99, 110, 'Fast wireless charging pad', 'ChargeTech', '2024-01-13'),
        ('Bluetooth Speaker', 'Electronics', 59.99, 85, 'Portable Bluetooth speaker', 'SoundWave', '2024-02-04'),
        ('Phone Stand', 'Electronics', 12.99, 200, 'Adjustable phone and tablet stand', 'StandPro', '2024-01-29'),
        ('Desk Fan', 'Appliances', 39.99, 70, 'Quiet desktop cooling fan', 'CoolBreeze', '2024-02-11'),
        ('Humidifier', 'Appliances', 69.99, 45, 'Ultrasonic desktop humidifier', 'AirCare', '2024-01-17'),
        ('Plant Pot', 'Decor', 16.99, 150, 'Ceramic plant pot with drainage', 'GreenThumb', '2024-02-22'),
        ('Wall Clock', 'Decor', 22.99, 90, 'Modern wall clock with silent movement', 'TimeStyle', '2024-01-24'),
        ('Picture Frame', 'Decor', 18.99, 130, '8x10 wooden picture frame', 'FrameCraft', '2024-02-06'),
        ('Candle Set', 'Decor', 26.99, 75, 'Scented candle set of 3', 'AromaLux', '2024-01-31'),
        ('Throw Pillow', 'Decor', 19.99, 100, 'Decorative throw pillow', 'HomeComfort', '2024-02-13'),
        ('Wall Art', 'Decor', 34.99, 60, 'Abstract canvas wall art', 'ArtSpace', '2024-01-21'),
        ('Desk Calendar', 'Office', 9.99, 200, '2024 desktop calendar', 'PlannerPro', '2024-02-19'),
        ('Notebook Set', 'Office', 15.99, 180, 'Set of 3 lined notebooks', 'WritePlus', '2024-01-27'),
        ('Pen Holder', 'Office', 11.99, 160, 'Wooden pen and pencil holder', 'DeskOrg', '2024-02-17'),
        ('Stapler', 'Office', 8.99, 220, 'Heavy-duty desktop stapler', 'OfficeTools', '2024-01-09'),
        ('Tape Dispenser', 'Office', 6.99, 250, 'Weighted tape dispenser', 'TapeTech', '2024-02-23'),
        ('Scissors', 'Office', 4.99, 300, '8-inch office scissors', 'CutPro', '2024-01-15'),
        ('Calculator', 'Office', 12.99, 140, 'Scientific calculator', 'MathTech', '2024-02-24')
    ]
    
    cursor.executemany('''
        INSERT INTO products (product_name, category, price, stock_quantity, description, supplier, created_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', products_data)

def populate_orders(cursor):
    """Populate orders table with sample data."""
    
    statuses = ['completed', 'pending', 'shipped', 'cancelled']
    orders_data = []
    
    for i in range(200):
        customer_id = random.randint(1, 100)
        order_date = datetime.now() - timedelta(days=random.randint(1, 365))
        total_amount = round(random.uniform(25, 1500), 2)
        status = random.choice(statuses)
        shipping_address = f"{random.randint(100,9999)} {random.choice(['Main', 'Oak', 'Pine', 'Elm', 'Cedar'])} St"
        
        orders_data.append((customer_id, order_date.date(), total_amount, status, shipping_address))
    
    cursor.executemany('''
        INSERT INTO orders (customer_id, order_date, total_amount, status, shipping_address)
        VALUES (?, ?, ?, ?, ?)
    ''', orders_data)

def populate_order_items(cursor):
    """Populate order_items table with sample data."""
    
    order_items_data = []
    
    for order_id in range(1, 201):  # For each order
        num_items = random.randint(1, 5)  # 1-5 items per order
        
        for _ in range(num_items):
            product_id = random.randint(1, 50)
            quantity = random.randint(1, 3)
            unit_price = round(random.uniform(5, 500), 2)
            total_price = round(unit_price * quantity, 2)
            
            order_items_data.append((order_id, product_id, quantity, unit_price, total_price))
    
    cursor.executemany('''
        INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price)
        VALUES (?, ?, ?, ?, ?)
    ''', order_items_data)

def populate_employees(cursor):
    """Populate employees table with sample data."""
    
    employees_data = [
        ('John', 'Smith', 'john.smith@company.com', 'Management', 'CEO', 150000.00, '2020-01-15', None),
        ('Sarah', 'Johnson', 'sarah.johnson@company.com', 'Management', 'CTO', 140000.00, '2020-02-01', 1),
        ('Michael', 'Brown', 'michael.brown@company.com', 'Management', 'CFO', 135000.00, '2020-03-15', 1),
        ('Emily', 'Davis', 'emily.davis@company.com', 'Engineering', 'Senior Developer', 95000.00, '2021-01-10', 2),
        ('David', 'Wilson', 'david.wilson@company.com', 'Engineering', 'Senior Developer', 92000.00, '2021-02-20', 2),
        ('Lisa', 'Garcia', 'lisa.garcia@company.com', 'Engineering', 'Developer', 75000.00, '2022-01-15', 4),
        ('Robert', 'Martinez', 'robert.martinez@company.com', 'Engineering', 'Developer', 73000.00, '2022-03-01', 4),
        ('Jessica', 'Anderson', 'jessica.anderson@company.com', 'Engineering', 'Junior Developer', 60000.00, '2023-01-10', 5),
        ('James', 'Taylor', 'james.taylor@company.com', 'Sales', 'Sales Manager', 85000.00, '2021-05-15', 1),
        ('Amanda', 'Thomas', 'amanda.thomas@company.com', 'Sales', 'Sales Rep', 55000.00, '2022-06-01', 9),
        ('William', 'Jackson', 'william.jackson@company.com', 'Sales', 'Sales Rep', 52000.00, '2022-08-15', 9),
        ('Ashley', 'White', 'ashley.white@company.com', 'Marketing', 'Marketing Manager', 80000.00, '2021-04-01', 1),
        ('Christopher', 'Harris', 'christopher.harris@company.com', 'Marketing', 'Marketing Specialist', 58000.00, '2022-09-01', 12),
        ('Nicole', 'Clark', 'nicole.clark@company.com', 'HR', 'HR Manager', 75000.00, '2021-03-15', 1),
        ('Richard', 'Lewis', 'richard.lewis@company.com', 'HR', 'HR Specialist', 50000.00, '2022-11-01', 14),
        ('Stephanie', 'Lee', 'stephanie.lee@company.com', 'Finance', 'Accountant', 65000.00, '2021-07-01', 3),
        ('Joseph', 'Walker', 'joseph.walker@company.com', 'Finance', 'Financial Analyst', 62000.00, '2022-04-15', 3),
        ('Elizabeth', 'Hall', 'elizabeth.hall@company.com', 'Customer Service', 'CS Manager', 55000.00, '2021-08-01', 1),
        ('Thomas', 'Allen', 'thomas.allen@company.com', 'Customer Service', 'CS Rep', 40000.00, '2023-02-01', 18),
        ('Jennifer', 'Young', 'jennifer.young@company.com', 'Customer Service', 'CS Rep', 38000.00, '2023-03-15', 18)
    ]
    
    cursor.executemany('''
        INSERT INTO employees (first_name, last_name, email, department, position, salary, hire_date, manager_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', employees_data)

if __name__ == "__main__":
    create_sample_database()