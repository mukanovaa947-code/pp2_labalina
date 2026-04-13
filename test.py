from connect import get_connection

conn = get_connection()
print("OK")
conn.close()