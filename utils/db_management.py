import sqlite3

db_name = r"C:\ProgramData\Jenkins\.jenkins\workspace\op-chapter-search\onepiece.db"

def get_connection():
    return sqlite3.connect(db_name)

def init_db():
    conn = get_connection()
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
        chapter_number INTEGER NOT NULL,
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
    conn.close()

def add_subscriber(email):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO subscribers (email) VALUES (?)", (email,))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Email already in the database")
    finally:
        conn.close()

def get_all_subscribers():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT email FROM subscribers")
    emails = [row[0] for row in cursor.fetchall()]
    conn.close()

    return emails

def save_chapter(chapter_number, week_found):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO chapters (chapter_number, week_found) VALUES (?, ?)", (chapter_number, week_found))
    conn.commit()
    chapter_id = cursor.lastrowid
    conn.close()

    return chapter_id

def get_link_chapter(chapter_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT source_name, url FROM chapter_links WHERE chapter_id = ?",
        (chapter_id,)
    )
    results = cursor.fetchall()
    conn.close()

    return [{"name": r[0], "url": r[1]} for r in results]

def save_links(chapter_id, links):
    conn = get_connection()
    cursor = conn.cursor()

    for link in links:
        cursor.execute(
            "INSERT INTO chapter_links (chapter_id, source_name, link) VALUES (?, ?, ?)",
            (chapter_id, link["name"], link["url"])
        )
    conn.commit()
    conn.close()

def check_chapter_found(week_found):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM chapters WHERE week_found = ?", (week_found,))
    result = cursor.fetchone()
    conn.close()

    return result is not None
