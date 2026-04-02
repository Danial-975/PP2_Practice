import psycopg2
from psycopg2 import extras

db_config = {
    "dbname": "phonebook_db",
    "user": "postgres",
    "password": "12345678d", 
    "host": "localhost",
    "port": "5432"
}

def manage_contacts():
    conn = None
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor(cursor_factory=extras.DictCursor)

        print("--- Executing Bulk Insert ---")
        names_list = ["John Doe", "System Admin", "User_3", "Invalid_Entry"]
        phones_list = ["79001112233", "79998887766", "1234567", "phone_abc"]
        
        cur.execute("CALL bulk_insert_contacts(%s, %s, NULL);", (names_list, phones_list))
        error_log = cur.fetchone()[0]
        
        if error_log:
            print("Validation errors found:")
            for error in error_log:
                print(f"  - {error}")
        else:
            print("All records processed successfully.")

        cur.execute("CALL upsert_contact(%s, %s);", ("John Updated", "79001112233"))

        search_term = "John"
        print(f"\n--- Search results for '{search_term}': ---")
        cur.execute("SELECT * FROM search_contacts(%s);", (search_term,))
        for row in cur.fetchall():
            print(f"ID: {row['id']} | Name: {row['name']} | Phone: {row['phone_number']}")

        limit, offset = 2, 0
        print(f"\n--- Pagination (Limit: {limit}, Offset: {offset}): ---")
        cur.execute("SELECT * FROM get_contacts_paged(%s, %s);", (limit, offset))
        for row in cur.fetchall():
            print(dict(row))

        cur.execute("CALL delete_contact_by_data(%s);", ("User_3",))
        
        conn.commit()
        print("\nDatabase transaction committed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    manage_contacts()