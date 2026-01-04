import sqlite3
from datetime import datetime
from typing import List, Dict, Any
import uuid

DB_PATH = "history.db"

def init_db():
    """Initialize the database with sessions and messages tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON")
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()

def create_session(title: str = "New Chat") -> str:
    """Create a new session and return its ID."""
    session_id = str(uuid.uuid4())
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO sessions (id, title) VALUES (?, ?)', (session_id, title))
    conn.commit()
    conn.close()
    return session_id

def get_sessions() -> List[Dict[str, Any]]:
    """Get all sessions ordered by creation time (newest first)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sessions ORDER BY created_at DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_session_messages(session_id: str) -> List[Dict[str, Any]]:
    """Get messages for a specific session."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM messages WHERE session_id = ? ORDER BY id ASC', (session_id,))
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        role = row['role']
        # Map for Gemini if needed, but we keep raw role here mostly
        if role == 'assistant': 
            role = 'model'
            
        history.append({
            "role": role,
            "content": row['content']
        })
    return history

def add_message(session_id: str, role: str, content: str):
    """Add a message to a specific session."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)', 
                   (session_id, role, content))
    conn.commit()
    conn.close()

def delete_session(session_id: str):
    """Delete a session and its messages."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')
    cursor.execute('DELETE FROM sessions WHERE id = ?', (session_id,))
    conn.commit()
    conn.close()

def update_session_title(session_id: str, title: str):
    """Update session title."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE sessions SET title = ? WHERE id = ?', (title, session_id))
    conn.commit()
    conn.close()
