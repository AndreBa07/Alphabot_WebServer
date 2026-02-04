from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3 as sql
import AlphaBot
import time
import hashlib
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

larry = AlphaBot.AlphaBot()
larry.stop()

app = Flask(__name__)
app.secret_key = "ChiaveSegreta"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    con = sql.connect("DB_utenti.db")
    cur = con.cursor()
    utente = cur.execute("SELECT utente FROM Utenti WHERE utente = ?", (user_id, )).fetchone()
    con.close()
    if utente:
        return User(user_id)
    return None

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        con = sql.connect("DB_utenti.db")
        cur = con.cursor()
        exists = cur.execute("SELECT password FROM Utenti WHERE utente = ? AND password = ?", (username, password_hash, )).fetchone()
        con.close()
        if exists:
            login_user(User(username))
            return redirect(url_for("control"))
    return render_template("login.html")

@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        con = sql.connect("DB_utenti.db")
        cur = con.cursor()
        exists = cur.execute("SELECT * FROM Utenti WHERE utente = ?", (username, )).fetchone()
        if not exists:
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            cur.execute("INSERT INTO Utenti(utente, password) VALUES (?, ?)", (username, password_hash, ))
            con.commit()
            con.close()

            login_user(User(username))
            return redirect(url_for("control"))
        else:
            con.close()
            flash(f"Utente {username} già esistente")
            return render_template("registration.html")
    return render_template("registration.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

con = sql.connect("movimenti_Larry.db") 
cur = con.cursor()
sequenza_quadrato = cur.execute(f"SELECT Sequenza FROM movimenti WHERE Tasto = ?", ("q", )).fetchall()
sequenza_triangolo = cur.execute(f"SELECT Sequenza FROM movimenti WHERE Tasto = ?", ("t", )).fetchall()
sequenza_rettangolo = cur.execute(f"SELECT Sequenza FROM movimenti WHERE Tasto = ?", ("r", )).fetchall() 
sequenza_cerchio = cur.execute(f"SELECT Sequenza FROM movimenti WHERE Tasto = ?", ("c", )).fetchall()
sequenza_integrale = cur.execute(f"SELECT Sequenza FROM movimenti WHERE Tasto = ?", ("i", )).fetchall() 
con.close()

def leggi_sequenza(sequenza):
    sequenza_split = sequenza[0][0].split(",")
    for i in range(0, len(sequenza_split), 2):
        comando = sequenza_split[i]
        tempo = sequenza_split[i + 1]
        if comando == "forward":
            larry.forward()
        elif comando == "backward":
            larry.backward()
        elif comando == "left":
            larry.left()
        elif comando == "right":
            larry.right()
        time.sleep(float(tempo))
        larry.stop()
            
            
@app.route("/control", methods=["GET", "POST"])
@login_required
def control():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "forward":
            larry.forward()
        elif action == "backward":
            larry.backward()
        elif action == "right":
            larry.right()
        elif action == "left":
            larry.left()
        elif action == "stop":
            larry.stop()
        elif action == "q": 
            leggi_sequenza(sequenza_quadrato)
        elif action == "r":
            leggi_sequenza(sequenza_rettangolo)
        elif action == "t":
            leggi_sequenza(sequenza_triangolo)
        elif action == "c":
            leggi_sequenza(sequenza_cerchio)
        elif action == "i":
            leggi_sequenza(sequenza_integrale)
        
    return render_template("control.html", user = current_user.id)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, use_reloader = False)