from database import add_contact, update_contact, search_contacts, delete_contact, import_from_csv

def menu():
    while True:
        print("\n--- PhoneBook Menu ---")
        print("1. Import from CSV")
        print("2. Add new contact (Console)")
        print("3. Update contact")
        print("4. Search contacts")
        print("5. Delete contact")
        print("0. Exit")
        
        choice = input("Select an option: ")

        if choice == "1":
            import_from_csv("data.csv")
        elif choice == "2":
            name = input("Enter name: ")
            phone = input("Enter phone: ")
            add_contact(name, phone)
        elif choice == "3":
            old_name = input("Enter the name of contact to update: ")
            new_name = input("Enter new name (leave blank to skip): ")
            new_phone = input("Enter new phone (leave blank to skip): ")
            update_contact(old_name, new_name if new_name else None, new_phone if new_phone else None)
        elif choice == "4":
            print("Search by: 1. Name  2. Phone Prefix")
            sub_choice = input("Choice: ")
            val = input("Enter search value: ")
            search_contacts("name" if sub_choice == "1" else "phone", val)
        elif choice == "5":
            val = input("Enter name or phone to delete: ")
            delete_contact(val)
        elif choice == "0":
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    menu()