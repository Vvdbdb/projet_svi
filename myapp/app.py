from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import mysql.connector
import os

app = Flask(__name__)
UPLOAD_FOLDER = "/var/lib/asterisk/sounds/temoignages"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="passer",  # Mets ton mot de passe ici si besoin
        database="safe_db"
    )

@app.route('/audios/<path:filename>')
def serve_audio(filename):
    return send_from_directory('/var/lib/asterisk/sounds/custom', filename)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/temoignages")
def temoignages():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM temoignages ORDER BY date DESC")
    temoignages = cursor.fetchall()
    conn.close()
    return render_template("temoignages.html", temoignages=temoignages)

@app.route("/callbacks")
def callbacks():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM callbacks ORDER BY date DESC")
    callbacks = cursor.fetchall()
    conn.close()
    return render_template("callbacks.html", callbacks=callbacks)

@app.route("/ecouter/<filename>")
def ecouter(filename):
    file_url = f"/temoignages_audio/{filename}"
    return render_template("ecouter.html", filename=file_url)

@app.route("/temoignages_audio/<filename>")
def temoignages_audio(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/supprimer/<int:id>")
def supprimer(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT filename FROM temoignages WHERE id = %s", (id,))
    result = cursor.fetchone()
    if result:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], result[0])
        if os.path.exists(filepath):
            os.remove(filepath)
    cursor.execute("DELETE FROM temoignages WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("temoignages"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
