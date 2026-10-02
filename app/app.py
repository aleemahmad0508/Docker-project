from flask import Flask, render_template, request, redirect, url_for
from database import get_db_connection

app = Flask(__name__)


@app.route("/")
def index():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, title, content FROM notes ORDER BY id DESC"
    )

    notes = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("index.html", notes=notes)


@app.route("/add", methods=["POST"])
def add_note():
    title = request.form["title"]
    content = request.form["content"]

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO notes (title, content) VALUES (%s, %s)",
        (title, content),
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("index"))


@app.route("/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM notes WHERE id = %s",
        (note_id,),
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("index"))


@app.route("/health")
def health():
    return {
        "status": "healthy",
        "application": "Docker Cloud Notes App"
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
