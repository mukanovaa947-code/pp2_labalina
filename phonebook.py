import csv
from connect import get_connection

conn = get_connection()
cur = conn.cursor()

# Создание таблицы
cur.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50),
    phone VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);
""")
conn.commit()

# Функции
def add_contact(first_name, last_name, phone, email=None):
    cur.execute("""
        INSERT INTO contacts (first_name, last_name, phone, email)
        VALUES (%s, %s, %s, %s)
        """, (first_name, last_name, phone, email))
    conn.commit()
    print(f"Contact {first_name} added!")

def import_from_csv(filename="contacts.csv"):
    with open(filename, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            first_name, last_name, phone = row
            add_contact(first_name, last_name, phone)

def update_contact_phone(first_name, new_phone):
    cur.execute("UPDATE contacts SET phone = %s WHERE first_name = %s",
                (new_phone, first_name))
    conn.commit()
    print("Phone updated!")

def search_by_name(name):
    cur.execute("SELECT * FROM contacts WHERE first_name LIKE %s OR last_name LIKE %s",
                (f"%{name}%", f"%{name}%"))
    return cur.fetchall()

def search_by_phone_prefix(prefix):
    cur.execute("SELECT * FROM contacts WHERE phone LIKE %s", (f"{prefix}%",))
    return cur.fetchall()

def delete_contact(phone):
    cur.execute("DELETE FROM contacts WHERE phone = %s", (phone,))
    conn.commit()
    print("Contact deleted!")

# Пример интерактивного меню
def menu():
    while True:
        print("\n1. Add contact")
        print("2. Import from CSV")
        print("3. Update contact phone")
        print("4. Search by name")
        print("5. Search by phone prefix")
        print("6. Delete contact")
        print("0. Exit")
        choice = input("Choose option: ")

        if choice == "1":
            fn = input("First name: ")
            ln = input("Last name: ")
            ph = input("Phone: ")
            add_contact(fn, ln, ph)
        elif choice == "2":
            import_from_csv()
        elif choice == "3":
            fn = input("First name to update: ")
            ph = input("New phone: ")
            update_contact_phone(fn, ph)
        elif choice == "4":
            name = input("Enter name: ")
            results = search_by_name(name)
            for r in results:
                print(r)
        elif choice == "5":
            prefix = input("Enter phone prefix: ")
            results = search_by_phone_prefix(prefix)
            for r in results:
                print(r)
        elif choice == "6":
            ph = input("Enter phone to delete: ")
            delete_contact(ph)
        elif choice == "0":
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    menu()
    cur.close()
    conn.close()