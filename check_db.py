import sqlite3

conn = sqlite3.connect("chat_history.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM messages")
rows = cursor.fetchall()

print("\n--- STORED MESSAGES ---\n")

for row in rows:
    print(row)

conn.close()