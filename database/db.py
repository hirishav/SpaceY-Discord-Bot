import sqlite3
import time
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "spacey.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def setup_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            coins INTEGER DEFAULT 0,
            xp INTEGER DEFAULT 0,
            horse_tier INTEGER DEFAULT 0
        )
    """)
    
    # Create inventory table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            user_id INTEGER,
            item_name TEXT,
            amount INTEGER DEFAULT 0,
            PRIMARY KEY (user_id, item_name)
        )
    """)
    
    # Create cooldowns table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cooldowns (
            user_id INTEGER,
            command TEXT,
            end_time REAL,
            PRIMARY KEY (user_id, command)
        )
    """)
    
    conn.commit()
    conn.close()

# Initialize on import
setup_db()

def _ensure_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

def add_coins(user_id: int, amount: int):
    _ensure_user(user_id)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET coins = coins + ? WHERE user_id = ?", (amount, user_id))
    cursor.execute("SELECT coins FROM users WHERE user_id = ?", (user_id,))
    coins = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return coins

def get_coins(user_id: int):
    _ensure_user(user_id)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT coins FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 0

def add_xp(user_id: int, amount: int):
    _ensure_user(user_id)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET xp = xp + ? WHERE user_id = ?", (amount, user_id))
    cursor.execute("SELECT xp FROM users WHERE user_id = ?", (user_id,))
    xp = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return xp

def set_cooldown(user_id: int, command: str, seconds: int):
    end_time = time.time() + seconds
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cooldowns (user_id, command, end_time) 
        VALUES (?, ?, ?) 
        ON CONFLICT(user_id, command) DO UPDATE SET end_time = ?
    """, (user_id, command, end_time, end_time))
    conn.commit()
    conn.close()

def get_cooldown(user_id: int, command: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT end_time FROM cooldowns WHERE user_id = ? AND command = ?", (user_id, command))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 0

def is_on_cooldown(user_id: int, command: str):
    return get_cooldown(user_id, command) > time.time()

def add_item(user_id: int, item: str, amount: int = 1):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO inventory (user_id, item_name, amount) 
        VALUES (?, ?, ?) 
        ON CONFLICT(user_id, item_name) DO UPDATE SET amount = amount + ?
    """, (user_id, item, amount, amount))
    conn.commit()
    conn.close()

def get_item_amount(user_id: int, item: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT amount FROM inventory WHERE user_id = ? AND item_name = ?", (user_id, item))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 0

def format_time_remaining(end_time):
    remaining = int(end_time - time.time())
    if remaining <= 0:
        return "Ready"
    
    hours, remainder = divmod(remaining, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0 or hours > 0:
        parts.append(f"{minutes}m")
    parts.append(f"{seconds}s")
    
    return " ".join(parts)
