from connect import get_connection

conn = get_connection()
cur = conn.cursor()

# 🔄 UPSERT
def upsert(first_name, last_name, phone, email=None):
    cur.execute(
        "CALL upsert_contact(%s, %s, %s, %s)",
        (first_name, last_name, phone, email)
    )
    conn.commit()


# 🔍 SEARCH FUNCTION
def search(pattern):
    cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
    return cur.fetchall()


# 📄 PAGINATION FUNCTION
def get_page(limit, offset):
    cur.execute("SELECT * FROM get_contacts_page(%s, %s)", (limit, offset))
    return cur.fetchall()


# ❌ DELETE PROCEDURE
def delete_by_name_or_phone(name=None, phone=None):
    cur.execute("CALL delete_contact(%s, %s)", (name, phone))
    conn.commit()


# 📦 BULK INSERT
def bulk_insert(data_list):
    cur.executemany(
        "INSERT INTO temp_contacts(first_name, last_name, phone) VALUES (%s, %s, %s)",
        data_list
    )
    conn.commit()

    cur.execute("CALL bulk_insert_contacts()")
    conn.commit()


# 🧪 TEST RUN
if __name__ == "__main__":

    print("🔄 UPSERT")
    upsert("Ali", "Khan", "99999", "ali@mail.com")

    print("\n🔍 SEARCH")
    print(search("Ali"))

    print("\n📄 PAGINATION")
    print(get_page(3, 0))

    print("\n📦 BULK INSERT")
    bulk_insert([
        ("John", "Doe", "11111"),
        ("Anna", "Smith", "22222"),
        ("Bad", "User", "abc123")
    ])

    print("\n❌ DELETE")
    delete_by_name_or_phone(name="Ali")

    cur.close()
    conn.close()