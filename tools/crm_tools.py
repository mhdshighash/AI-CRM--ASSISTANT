import sqlite3
#get customer deals by name
def get_customer_deals(customer_name):

    connection = sqlite3.connect("crm.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT customers.name,
               deals.title,
               deals.value,
               deals.status
        FROM customers
        JOIN deals
        ON customers.id = deals.customer_id
        WHERE customers.name = ?
    """, (customer_name,))

    results = cursor.fetchall()

    connection.close()

    return results

#get deals by status
def get_deals_by_status(status):

    connection = sqlite3.connect("crm.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT customers.name,
               deals.title,
               deals.value,
               deals.status
        FROM customers
        JOIN deals
        ON customers.id = deals.customer_id
        WHERE deals.status = ?
    """, (status,))

    results = cursor.fetchall()

    connection.close()

    return results


#update deal status
def update_deal_status(deal_id, new_status):

    allowed_statuses = ["New", "Contacted", "Won", "Lost"]

    if new_status not in allowed_statuses:
        return "Invalid status. Choose New, Contacted, Won, or Lost."

    connection = sqlite3.connect("crm.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE deals
        SET status = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (new_status, deal_id))

    connection.commit()

    if cursor.rowcount == 0:
        connection.close()
        return "Deal not found."

    connection.close()

    return "Deal updated successfully."

# =========================
# 4. ADD CUSTOMER NOTE
# =========================

def add_note(customer_id, note):

    connection = sqlite3.connect("crm.db")

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO notes (customer_id, note)
        VALUES (?, ?)
    """, (customer_id, note))

    connection.commit()

    connection.close()

    return "Note added successfully."

# Get customer ID by customer name
def get_customer_id_by_name(customer_name):

    connection = sqlite3.connect("crm.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM customers
        WHERE name = ?
    """, (customer_name,))

    result = cursor.fetchone()

    connection.close()

    if result is None:
        return None

    return result[0]
def add_note_by_customer_name(customer_name, note):

    customer_id = get_customer_id_by_name(customer_name)

    if customer_id is None:
        return f"Customer '{customer_name}' not found."

    return add_note(customer_id, note)

# Get all notes for a customer
def get_customer_notes(customer_name):

    customer_id = get_customer_id_by_name(customer_name)

    if customer_id is None:
        return f"Customer '{customer_name}' not found."

    connection = sqlite3.connect("crm.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, note, created_at
        FROM notes
        WHERE customer_id = ?
        ORDER BY created_at DESC
    """, (customer_id,))

    results = cursor.fetchall()

    connection.close()

    return results
# Get all customers
def get_all_customers():

    connection = sqlite3.connect("crm.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, email, company
        FROM customers
        ORDER BY id
    """)

    results = cursor.fetchall()

    connection.close()

    return results