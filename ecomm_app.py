import sqlite3

DB_NAME = "ecommerce.db"

# -------------------- Database Connection --------------------
def connect_db():
    return sqlite3.connect(DB_NAME)

# -------------------- Create Tables --------------------
def create_tables():
    conn = connect_db()
    cur = conn.cursor()

    # Users
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        password TEXT,
        street TEXT,
        city TEXT,
        zip TEXT,
        createdAt DATE
    )""")

    # Products
    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        category TEXT,
        price REAL,
        stock INTEGER
    )""")

    # Orders
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        userId INTEGER,
        totalAmount REAL,
        status TEXT,
        createdAt DATE,
        FOREIGN KEY(userId) REFERENCES users(id)
    )""")

    # Order Items
    cur.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        orderId INTEGER,
        productId INTEGER,
        qty INTEGER,
        price REAL,
        FOREIGN KEY(orderId) REFERENCES orders(id),
        FOREIGN KEY(productId) REFERENCES products(id)
    )""")

    # Reviews
    cur.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY,
        productId INTEGER,
        userId INTEGER,
        rating INTEGER,
        comment TEXT,
        createdAt DATE,
        FOREIGN KEY(productId) REFERENCES products(id),
        FOREIGN KEY(userId) REFERENCES users(id)
    )""")

    conn.commit()
    conn.close()
    print("Tables created successfully!")

# -------------------- Insert Sample Data --------------------
def insert_sample_data():
    conn = connect_db()
    cur = conn.cursor()

    # Users
    users = [
        (1,'Alice Johnson','alice@example.com','alice123','123 Main St','New York','10001','2024-01-10'),
        (2,'Bob Smith','bob@example.com','bob456','456 Oak Ave','Los Angeles','90001','2024-02-15'),
        (3,'Charlie Brown','charlie@example.com','charlie789','789 Pine Rd','Chicago','60601','2024-03-12'),
        (4,'David Miller','david@example.com','david321','321 Maple Blvd','Houston','77001','2024-04-20'),
        (5,'Eva Green','eva@example.com','eva654','654 Cedar Ln','San Francisco','94101','2024-05-05')
    ]
    cur.executemany("INSERT OR IGNORE INTO users VALUES (?,?,?,?,?,?,?,?)", users)

    # Products
    products = [
        (101,'Laptop Pro 15','High performance laptop','Electronics',1200,50),
        (102,'Wireless Mouse','Ergonomic wireless mouse','Electronics',25,200),
        (103,'Office Chair','Comfortable office chair','Furniture',150,80),
        (104,'Coffee Mug','Ceramic coffee mug','Home',10,500),
        (105,'Smartphone X','Latest generation smartphone','Electronics',900,100),
        (106,'Headphones','Noise cancelling headphones','Electronics',200,120),
        (107,'Bookshelf','Wooden bookshelf','Furniture',180,30),
        (108,'Table Lamp','LED desk lamp','Home',40,150),
        (109,'Backpack','Waterproof backpack','Fashion',60,75),
        (110,'Sneakers','Running sneakers','Fashion',120,60)
    ]
    cur.executemany("INSERT OR IGNORE INTO products VALUES (?,?,?,?,?,?)", products)

    # Orders
    orders = [
        (201,1,1250,'shipped','2024-06-10'),
        (202,2,1100,'pending','2024-06-15'),
        (203,3,190,'delivered','2024-06-18'),
        (204,1,60,'shipped','2024-07-01'),
        (205,5,240,'delivered','2024-07-05')
    ]
    cur.executemany("INSERT OR IGNORE INTO orders VALUES (?,?,?,?,?)", orders)

    # Order Items
    order_items = [
        (201,101,1,1200),
        (201,102,2,25),
        (202,105,1,900),
        (202,106,1,200),
        (203,103,1,150),
        (203,104,4,10),
        (204,109,1,60),
        (205,110,2,120)
    ]
    cur.executemany("INSERT OR IGNORE INTO order_items VALUES (?,?,?,?)", order_items)

    # Reviews
    reviews = [
        (301,101,1,5,'Excellent laptop','2024-06-12'),
        (302,102,2,4,'Good mouse but battery drains fast','2024-06-16'),
        (303,105,3,5,'Amazing smartphone','2024-06-20'),
        (304,103,4,3,'Chair is okay but a bit pricey','2024-06-22'),
        (305,106,5,4,'Sound quality is great','2024-06-25')
    ]
    cur.executemany("INSERT OR IGNORE INTO reviews VALUES (?,?,?,?,?,?)", reviews)

    conn.commit()
    conn.close()
    print("Sample data inserted successfully!")

# -------------------- CRUD Operations --------------------

# Users
def view_users():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    for r in rows:
        print(r)
    conn.close()

def add_user():
    conn = connect_db()
    cur = conn.cursor()
    name = input("Name: ")
    email = input("Email: ")
    password = input("Password: ")
    street = input("Street: ")
    city = input("City: ")
    zip_code = input("ZIP: ")
    createdAt = input("CreatedAt (YYYY-MM-DD): ")
    cur.execute("INSERT INTO users (name,email,password,street,city,zip,createdAt) VALUES (?,?,?,?,?,?,?,?)",
                (name,email,password,street,city,zip_code,createdAt))
    conn.commit()
    conn.close()
    print("User added successfully!")

def update_user_email_password():
    user_id = int(input("Enter user ID to update: "))
    email = input("New Email: ")
    password = input("New Password: ")
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET email=?, password=? WHERE id=?", (email,password,user_id))
    conn.commit()
    conn.close()
    print("User updated successfully!")

def delete_user():
    user_id = int(input("Enter user ID to delete: "))
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    print("User deleted successfully!")

# Products
def view_products():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    for r in rows:
        print(r)
    conn.close()

def update_stock(product_id, qty):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (qty, product_id))
    conn.commit()
    conn.close()
    print(f"Stock of product {product_id} reduced by {qty}")

# -------------------- Menu --------------------
def menu():
    while True:
        print("\n===== E-Commerce CRUD Menu =====")
        print("1. View Users")
        print("2. Add User")
        print("3. Update User Email/Password")
        print("4. Delete User")
        print("5. View Products")
        print("6. Update Product Stock")
        print("7. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            view_users()
        elif choice == "2":
            add_user()
        elif choice == "3":
            update_user_email_password()
        elif choice == "4":
            delete_user()
        elif choice == "5":
            view_products()
        elif choice == "6":
            pid = int(input("Product ID: "))
            qty = int(input("Qty to reduce: "))
            update_stock(pid, qty)
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

# -------------------- Main --------------------
if __name__ == "__main__":
    create_tables()
    insert_sample_data()
    menu()
