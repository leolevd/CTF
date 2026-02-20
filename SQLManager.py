import sqlite3
from randomGOODpasswordGeNeRaToR import generate_password as makepass

DB_PATH = "data.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def initialize_db():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            role TEXT
        )
        """)
        conn.commit()

def add_default_users():
    users = [
        (1, "admin", "adminrules-" + makepass(), "admin"),
        (2, "Leo", makepass(), "admin"),
        (3, "Alice", makepass(), "user"),
        (4, "Bob", makepass(), "user"),
        (5, "Craze", makepass(), "manager"),
        (6, "Grace", makepass(), "manager"),
        (7, "Buff", makepass(), "user"),
        (8, "Nu11Byt3", makepass(50), "top_admin"),
        (9, "Grook", makepass(), "user"),
        (10, "George", "qwerty123", "user")
    ]
    with get_connection() as conn:
        cur = conn.cursor()
        for u in users:
            cur.execute("INSERT OR IGNORE INTO users (id, username, password, role) VALUES (?, ?, ?, ?)", u)
        conn.commit()

# --- LOGIN ---
def vulnerable_login(u: str, p: str):
    query = f"SELECT * FROM users WHERE username='{u}' AND password='{p}'"
    with get_connection() as conn:

        cur = conn.cursor()
        res = cur.execute(query).fetchone()

    if res:
        return True, res[3]
    return False, ""

def safe_login(u: str, p: str):
    query = "SELECT * FROM users WHERE username=? AND password=?"
    with get_connection() as conn:
        try:
            cur = conn.cursor()
            res = cur.execute(query, (u, p)).fetchone()
        except Exception:
            return False, ""
    if res:
        return True, res[3]
    return False, ""

# --- USER MANAGEMENT ---
def add_user(username: str, password: str, role: str):
    if role not in ["user", "manager", "admin", "top_admin"]:
        return False
    with get_connection() as conn:
        cur = conn.cursor()
        r = cur.execute("SELECT username FROM users").fetchall()
        if (username,) in r:
            return False
        cur.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        conn.commit()

def update_role(username: str, newrole: str):
    with get_connection() as conn:
        if newrole not in ["user", "manager", "admin", "top_admin"]:
            return False
        cur = conn.cursor()
        cur.execute("UPDATE users SET role=? WHERE username=?", (newrole, username))
        conn.commit()



def delete_user(username: str):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE username=?", (username,))
        conn.commit()

def get_user_id(username: str):
    with get_connection() as conn:
        cur = conn.cursor()
        res = cur.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
    if res:
        return res[0]
    return None

def delete_user_by_id(user_id: int):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()

def hard_RESET():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS users")
        cur.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            role TEXT
        )
        """)
        conn.commit()
    add_default_users()

# --- INITIALIZATION ---
hard_RESET()
initialize_db()
add_default_users()
