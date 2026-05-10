from flask import Flask, request
import sqlite3
from contextlib import contextmanager
import os

app = Flask(__name__)
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
@app.route("/")
def home():
    return "One Piece Search Home"

@app.route("/unsubscribe")
def unsubscribe():
    token = request.args.get("token")

    with get_db() as conn:
        cursor = conn.cursor()

        cursor.execute("UPDATE subscribers SET active = 0 WHERE token = ? AND active = 1", (token,))
        conn.commit()

        if cursor.rowcount == 0:
            return "No encontramos tu usuario. Ya estás dado de baja", 404

        return "Dejaste de buscar el One Piece! Te esperaremos en Laugh Tale"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
