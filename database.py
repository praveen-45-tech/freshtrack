import sqlite3


def create_table():

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT,
        email TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_user(username, password, email):

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    try:

        c.execute(
            """
            INSERT INTO users(username,password,email)
            VALUES(?,?,?)
            """,
            (username, password, email)
        )

        conn.commit()
        conn.close()

        return True

    except sqlite3.IntegrityError:

        conn.close()

        return False


def login_user(username, password):

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute(
        """
        SELECT *
        FROM users
        WHERE username=? AND password=?
        """,
        (username, password)
    )

    data = c.fetchone()

    conn.close()

    return data is not None


def get_email(username):

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute(
        """
        SELECT email
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    data = c.fetchone()

    conn.close()

    if data:
        return data[0]

    return None


def user_exists(username):

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute(
        """
        SELECT username
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    data = c.fetchone()

    conn.close()

    return data is not None


def get_all_users():

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute(
        """
        SELECT username,email
        FROM users
        """
    )

    data = c.fetchall()

    conn.close()

    return data


def delete_user(username):

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute(
        """
        DELETE FROM users
        WHERE username=?
        """,
        (username,)
    )

    conn.commit()
    conn.close()
