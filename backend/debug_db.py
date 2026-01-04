import sqlite3
import os

DB_PATH = "history.db"

def dump_db():
    if not os.path.exists(DB_PATH):
        print("Database not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("--- SESSIONS (Last 3) ---")
    cursor.execute("SELECT * FROM sessions ORDER BY created_at DESC LIMIT 3")
    sessions = cursor.fetchall()
    for s in sessions:
        print(f"ID: {s['id']}, Title: {s['title']}")

    if sessions:
        last_session_id = sessions[0]['id']
        print(f"\n--- MESSAGES for Session {last_session_id} ---")
        cursor.execute("SELECT * FROM messages WHERE session_id = ? ORDER BY id ASC", (last_session_id,))
        messages = cursor.fetchall()
        for m in messages:
            print(f"[{m['role']}] {m['content']}")

    conn.close()

if __name__ == "__main__":
    dump_db()
