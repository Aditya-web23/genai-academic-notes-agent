import sqlite3

# Create connection
conn = sqlite3.connect("chat_history.db", check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    thread_id TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()


# Save message
def save_message(thread_id, role, content):
    cursor.execute(
        "INSERT INTO messages (thread_id, role, content) VALUES (?, ?, ?)",
        (thread_id, role, content),
    )
    conn.commit()


# Load messages
def load_messages(thread_id):
    cursor.execute(
        "SELECT role, content FROM messages WHERE thread_id=?",
        (thread_id,),
    )
    return cursor.fetchall()

def get_all_messages():
    cursor.execute("""
        SELECT id, thread_id, role, content, created_at 
        FROM messages
        ORDER BY created_at DESC
    """)
    return cursor.fetchall()