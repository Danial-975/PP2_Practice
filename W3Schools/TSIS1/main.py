import json
import csv
import os
from connect import DatabaseManager

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "contacts.csv")

class ContactApp:
    def __init__(self):
        self.db = DatabaseManager()

    # --- Search and Pagination ---
    def search(self):
        query = input("Enter search term (name/email/phone): ")
        results = self.db.execute_query("SELECT * FROM search_contacts(%s) ORDER BY contact_id ASC", (query,))
        
        print("\nSearch Results:")
        if not results:
            print("No contacts found.")
        for r in results:
            print(f"[{r['contact_id']}] {r['name']} - {r['email']} - {r['phone']}")

    def list_paged(self):
        sort_map = {"1": "name", "2": "birthday", "3": "c.id"}
        print("\nSort by: 1. Name | 2. Birthday | 3. Date Added (ID)")
        choice = input("Select (1-3): ")
        col = sort_map.get(choice, "name")
        
        page = 1
        limit = 5
        while True:
            offset = (page - 1) * limit
            rows = self.db.execute_query(
                f"SELECT c.name, c.email, c.birthday, g.name as gname "
                f"FROM contacts c "
                f"LEFT JOIN groups g ON c.group_id = g.id "
                f"ORDER BY {col} LIMIT %s OFFSET %s", (limit, offset)
            )
            
            print(f"\n--- Page {page} ---")
            if not rows:
                print("No more records.")
            for r in rows:
                print(f"{r['name']} | {r['email']} | {r['birthday']} | Group: {r['gname']}")
            
            cmd = input("\n[n] Next, [p] Previous, [q] Back to Menu: ").lower()
            if cmd == 'n': page += 1
            elif cmd == 'p' and page > 1: page -= 1
            elif cmd == 'q': break

    # --- Import / Export ---
    def export_to_json(self):
        sql = """
            SELECT c.name, c.email, c.birthday, g.name as group_name,
            (SELECT json_agg(p.*) FROM phones p WHERE p.contact_id = c.id) as phones
            FROM contacts c LEFT JOIN groups g ON c.group_id = g.id
            ORDER BY c.id ASC"""
        data = self.db.execute_query(sql)
        with open("contacts.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, default=str, ensure_ascii=False)
        print("Export successful: contacts.json created.")

    def import_from_json(self):
        if not os.path.exists("contacts.json"):
            print("Error: contacts.json not found.")
            return
            
        with open("contacts.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                # Handle group and basic info
                self.db.call_proc("move_to_group", (item['name'], item.get('group_name', 'Other')))
                self.db.execute_query(
                    "UPDATE contacts SET email=%s, birthday=%s WHERE name=%s",
                    (item.get('email'), item.get('birthday'), item['name']), fetch=False
                )
                # Handle phones if present
                if item.get('phones'):
                    for p in item['phones']:
                        self.db.call_proc("add_phone", (item['name'], p['phone'], p['type']))
        print("JSON Import completed.")

    def import_from_csv(self):
        if not os.path.exists("contacts.csv"):
            print("Error: contacts.csv not found.")
            return

        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                exists = self.db.execute_query("SELECT id FROM contacts WHERE name = %s", (row['name'],))
                if not exists:
                    self.db.execute_query("INSERT INTO contacts (name) VALUES (%s)", (row['name'],), fetch=False)
                    print(f"Created new contact: {row['name']}")

                self.db.call_proc("move_to_group", (row['name'], row['group']))
                
                self.db.execute_query(
                    "UPDATE contacts SET email=%s, birthday=%s WHERE name=%s",
                    (row['email'], row['birthday'], row['name']), fetch=False
                )

                self.db.call_proc("add_phone", (row['name'], row['phone'], row['type']))
        print("\nCSV Import completed successfully!")
    
    def filter_by_group(self):
        groups = self.db.execute_query("SELECT name FROM groups ORDER BY name")
        if not groups:
            print("Groups not found.")
            return
        print("\nSelect a category:")
        for idx, g in enumerate(groups, 1):
            print(f"{idx}. {g['name']}")
        choice = input("Enter number: ")
        try:
            selected_group = groups[int(choice)-1]['name']
            query = """
                SELECT c.id, c.name, c.email, g.name as group_name
                FROM contacts c
                JOIN groups g ON c.group_id = g.id
                WHERE g.name = %s
            """
            results = self.db.execute_query(query, (selected_group,))
            print(f"\n--- Group: {selected_group} ---")
            for r in results:
                print(f"[{r['id']}] {r['name']} - {r['email']}")
        except (ValueError, IndexError):
            print("Invalid choice.")

    def add_phone_to_contact(self):
        print("\n--- Add Phone Number ---")
        name = input("Enter contact name: ")
        phone = input("Enter phone number: ")
        p_type = input("Enter type (home/work/mobile): ").lower()
        if p_type not in ['home', 'work', 'mobile']:
            print("Error: Invalid type! Use home, work, or mobile.")
            return
        self.db.execute_query("CALL add_phone(%s, %s, %s)", (name, phone, p_type))
        print(f"Phone {phone} added to {name} (if contact exists).")

    def move_contact_to_group(self):
        print("\n--- Change Contact Group ---")
        name = input("Enter contact name: ")
        group = input("Enter new group name: ")
        self.db.execute_query("CALL move_to_group(%s, %s)", (name, group))
        print(f"Contact {name} moved to group '{group}'.")

    # --- Main Menu ---
    def run(self):
        while True:
            print("\n--- Phonebook Manager Pro ---")
            print("1. Advanced Search")
            print("2. Paginated List")
            print("3. Export to JSON")
            print("4. Import from JSON")
            print("5. Import from CSV")
            print("6. Add phone number") 
            print("7. Change group")
            print("0. Exit")
            
            choice = input("\nSelect an option: ")
            if choice == "1": self.search()
            elif choice == "2": self.list_paged()
            elif choice == "3": self.export_to_json()
            elif choice == "4": self.import_from_json()
            elif choice == "5": self.import_from_csv()
            elif choice == "6": self.add_phone_to_contact()
            elif choice == "7": self.move_contact_to_group()
            elif choice == "0": 
                print("Goodbye!")
                break
            else:
                print("Invalid choice, try again.")

if __name__ == "__main__":
    app = ContactApp()
    app.run()