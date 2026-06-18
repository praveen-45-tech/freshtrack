

import sqlite3

def create_table():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    try:
        c.execute(
            "INSERT INTO users VALUES (?, ?)",
            (username.strip(), password.strip())
        )
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def login_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username.strip(), password.strip())
    )

    data = c.fetchone()
    conn.close()

    return data is not None
