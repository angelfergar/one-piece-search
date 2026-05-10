import sqlite3
from contextlib import contextmanager

db_name = r"C:\jenkins_data\onepiece.db"

def get_connection():
    return sqlite3.connect(db_name)

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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL)
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS chapters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chapter_number INTEGER,
            week_found TEXT NOT NULL,
            found_at TIME DEFAULT CURRENT_TIMESTAMP)
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS chapter_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chapter_id INTEGER,
            source_name TEXT,
            link TEXT,
            FOREIGN KEY (chapter_id) REFERENCES chapters(id))
            """
        )

        conn.commit()

def add_subscriber(email):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO subscribers (email) VALUES (?)", (email,))
            conn.commit()
        except sqlite3.IntegrityError:
            print("Email already in the database")

def get_all_subscribers():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM subscribers")
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
