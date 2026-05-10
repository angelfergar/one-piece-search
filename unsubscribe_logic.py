from flask import Flask, request
from utils.db_management import get_db
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "One Piece Search Home"

@app.route("/unsubscribe")
def unsubscribe():
    token = request.args.get("token")

    with get_db() as conn:
        cursor = conn.cursor()

        cursor.execute("UPDATE subscribers SET active = 0 WHERE token = %s AND active = 1", (token,))
        conn.commit()

        if cursor.rowcount == 0:
            return "No encontramos tu usuario. Ya estás dado de baja", 404

        return "Dejaste de buscar el One Piece! Te esperaremos en Laugh Tale"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


