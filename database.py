import psycopg2
import streamlit as st


def get_connection():
    return psycopg2.connect(st.secrets["DB_URL"])


def create_table():

    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT,
        email TEXT
    )
    """)

    conn.commit()
    c.close()
    conn.close()


def add_user(username, password, email):

    conn = get_connection()
    c = conn.cursor()

    try:

        c.execute(
            """
            INSERT INTO users(username,password,email)
            VALUES(%s,%s,%s)
            """,
            (username, password, email)
        )

        conn.commit()
        c.close()
        conn.close()

        return True

    except psycopg2.errors.UniqueViolation:

        conn.rollback()
        c.close()
        conn.close()

        return False


def login_user(username, password):

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        """
        SELECT *
        FROM users
        WHERE username=%s AND password=%s
        """,
        (username, password)
    )

    data = c.fetchone()

    c.close()
    conn.close()

    return data is not None


def get_email(username):

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        """
        SELECT email
        FROM users
        WHERE username=%s
        """,
        (username,)
    )

    data = c.fetchone()

    c.close()
    conn.close()

    if data:
        return data[0]

    return None


def user_exists(username):

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        """
        SELECT username
        FROM users
        WHERE username=%s
        """,
        (username,)
    )

    data = c.fetchone()

    c.close()
    conn.close()

    return data is not None


def get_all_users():

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        """
        SELECT username,email
        FROM users
        """
    )

    data = c.fetchall()

    c.close()
    conn.close()

    return data


def delete_user(username):

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        """
        DELETE FROM users
        WHERE username=%s
        """,
        (username,)
    )

    conn.commit()
    c.close()
    conn.close()
