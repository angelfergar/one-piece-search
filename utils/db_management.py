import psycopg2
from contextlib import contextmanager
import secrets
from flask import url_for
import os

def get_connection():
    return psycopg2.connect(os.environ["db_name"])

@contextmanager
def get_db():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS subscribers (
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            token TEXT UNIQUE,
            active INTEGER DEFAULT 1)
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS chapters (
            id SERIAL PRIMARY KEY,
            chapter_number INTEGER,
            week_found TEXT NOT NULL,
            found_at TIME DEFAULT CURRENT_TIMESTAMP)
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS chapter_links (
            id SERIAL PRIMARY KEY,
            chapter_id INTEGER,
            source_name TEXT,
            link TEXT,
            FOREIGN KEY (chapter_id) REFERENCES chapters(id))
            """
        )

        conn.commit()

def generate_token():
    return secrets.token_urlsafe(32)

def add_subscriber(email):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            token = generate_token()
            cursor.execute("INSERT INTO subscribers (email, token) VALUES (?,?)", (email,token))
            conn.commit()
        except psycopg2.IntegrityError:
            print("Email already in the database")

def get_all_subscribers():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT email, token FROM subscribers WHERE active = 1")
        emails = [row[0] for row in cursor.fetchall()]
        return emails

def save_chapter(chapter_number, week_found):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chapters (chapter_number, week_found) VALUES (?, ?)", (chapter_number, week_found))
        conn.commit()
        chapter_id = cursor.lastrowid
        return chapter_id

def save_links(chapter_id, links):
    with get_db() as conn:
        cursor = conn.cursor()
        for link in links:
            cursor.execute(
                "INSERT INTO chapter_links (chapter_id, source_name, link) VALUES (?, ?, ?)",
                (chapter_id, link["name"], link["url"])
            )
        conn.commit()

def check_chapter_found(week_found):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM chapters WHERE week_found = ?", (week_found,))
        result = cursor.fetchone()
        return result is not None

def generate_unsubscribe_link():
    unsubscribe_link = {}
    for email, token in get_all_subscribers():
        link = url_for("unsubscribe", token=token, _external=True)
        unsubscribe_link[email] = link

    return unsubscribe_link




