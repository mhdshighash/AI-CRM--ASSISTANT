import sqlite3

# Connect to the database
connection = sqlite3.connect("crm.db")

# Create a cursor
cursor = connection.cursor()


#1. CREATE CUSTOMERS TABLE

cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT,
        company TEXT
    )
""")


# 2. ADD CUSTOMERS

cursor.execute("""
    INSERT INTO customers (name, email, company)
    VALUES (?, ?, ?)
""", ("Mohamed", "mhd@gmail.com", "MHD Technologies"))

cursor.execute("""
    INSERT INTO customers (name, email, company)
    VALUES (?, ?, ?)
""", ("Mani", "mani@gmail.com", "ManiTech Solutions"))

cursor.execute("""
    INSERT INTO customers (name, email, company)
    VALUES (?, ?, ?)
""", ("Thomas", "thomas@gmail.com", "Robinson Ltd"))


# 3. CREATE DEALS TABLE

cursor.execute("""
    CREATE TABLE IF NOT EXISTS deals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        value REAL NOT NULL,
        status TEXT NOT NULL,
        salesperson TEXT,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    )
""")


# 4. ADD DEALS

cursor.execute("""
    INSERT INTO deals
    (customer_id, title, value, status, salesperson)
    VALUES (?, ?, ?, ?, ?)
""", (1, "AI Software", 150000, "Contacted", "Rachel"))

cursor.execute("""
    INSERT INTO deals
    (customer_id, title, value, status, salesperson)
    VALUES (?, ?, ?, ?, ?)
""", (2, "Data Analytics", 80000, "New", "Sowmiya"))

cursor.execute("""
    INSERT INTO deals
    (customer_id, title, value, status, salesperson)
    VALUES (?, ?, ?, ?, ?)
""", (3, "CRM Platform", 200000, "Won", "Rachel"))


# 5. CREATE NOTES TABLE

cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        note TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    )
""")


# 6. ADD SAMPLE NOTES

cursor.execute("""
    INSERT INTO notes (customer_id, note)
    VALUES (?, ?)
""", (1, "Discussed pricing with customer"))

cursor.execute("""
    INSERT INTO notes (customer_id, note)
    VALUES (?, ?)
""", (1, "Customer requested a product demo"))

cursor.execute("""
    INSERT INTO notes (customer_id, note)
    VALUES (?, ?)
""", (2, "Customer is interested in data analytics"))

cursor.execute("""
    INSERT INTO notes (customer_id, note)
    VALUES (?, ?)
""", (3, "Customer accepted the CRM proposal"))


# 7. SAVE EVERYTHING

connection.commit()


# 8. DISPLAY CUSTOMERS

print("\nCustomers:")

cursor.execute("SELECT * FROM customers")

customers = cursor.fetchall()

for customer in customers:
    print(customer)

# 9. DISPLAY DEALS

print("\nDeals:")

cursor.execute("SELECT * FROM deals")

deals = cursor.fetchall()

for deal in deals:
    print(deal)


# 10. DISPLAY NOTES

print("\nNotes:")

cursor.execute("SELECT * FROM notes")

notes = cursor.fetchall()

for note in notes:
    print(note)


#11.Close database
connection.close()