import psycopg2
import csv
import os

DB_CONFIG = {
    "dbname": "phonebook_db",
    "user": "postgres",
    "password": "12345678d", 
    "host": "localhost",
    "port": "5432"
}

def import_from_csv(file_path):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                if not os.path.exists(file_path):
                    print(f"File {file_path} not found.")
                    return
                with open(file_path, mode='r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        cur.execute(
                            "INSERT INTO contacts (name, phone_number) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                            (row['name'], row['phone_number'])
                        )
                conn.commit()
                print(f"Data imported from {file_path} successfully!")
    except Exception as e:
        print(f"Import error: {e}")

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

# 1. Insert from Console
def add_contact(name, phone):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO contacts (name, phone_number) VALUES (%s, %s)",
                    (name, phone)
                )
                conn.commit()
                print(f"Contact {name} added successfully!")
    except Exception as e:
        print(f"Error adding contact: {e}")

# 2. Update contact (Name or Phone)
def update_contact(old_name, new_name=None, new_phone=None):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                if new_name:
                    cur.execute("UPDATE contacts SET name = %s WHERE name = %s", (new_name, old_name))
                if new_phone:
                    cur.execute("UPDATE contacts SET phone_number = %s WHERE name = %s", (new_phone, old_name))
                conn.commit()
                print(f"Contact {old_name} updated!")
    except Exception as e:
        print(f"Update error: {e}")

# 3. Query/Filter contacts
def search_contacts(filter_type, value):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                if filter_type == "name":
                    cur.execute("SELECT * FROM contacts WHERE name ILIKE %s", (f"%{value}%",))
                elif filter_type == "phone":
                    cur.execute("SELECT * FROM contacts WHERE phone_number LIKE %s", (f"{value}%",))
                
                results = cur.fetchall()
                for row in results:
                    print(row)
    except Exception as e:
        print(f"Search error: {e}")

# 4. Delete contact
def delete_contact(name_or_phone):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM contacts WHERE name = %s OR phone_number = %s",
                    (name_or_phone, name_or_phone)
                )
                conn.commit()
                print(f"Contact deleted!")
    except Exception as e:
        print(f"Delete error: {e}")