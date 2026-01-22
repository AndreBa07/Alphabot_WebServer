from flask import Flask, request, render_template, redirect, url_for
import sqlite3 as sql
import AlphaBot
import time
import secrets
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

USERS = { # Sostituire con sqlite3
    "admin": {"password": "alphabot"} # Fare una query che restituisce tutti gli utenti poi fare un for
}

@login_manager.user_loader
def load_user(user_id):
    if user_id in USERS:
        return User(user_id)
    return None
# METTERE QUI ROTTA INDEX "/"
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Query per verificare che esista l'utente
        if username in USERS and USERS[username]["password"] == password:
            login_user(User(username))
            return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

con = sql.connect("movimenti_Larry.db") 
cur = con.cursor()
sequenza_q = cur.execute(f"SELECT Sequenza FROM movimenti WHERE Tasto = ?", ("q", )) 
sequenza_quadrato = sequenza_q.fetchall() 
sequenza_t = cur.execute(f"SELECT Sequenza FROM movimenti WHERE Tasto = ?", ("t", )) 
sequenza_triangolo = sequenza_t.fetchall() 
sequenza_r = cur.execute(f"SELECT Sequenza FROM movimenti WHERE Tasto = ?", ("r", )) 
sequenza_rettangolo = sequenza_r.fetchall() 
sequenza_c = cur.execute(f"SELECT Sequenza FROM movimenti WHERE Tasto = ?", ("c", )) 
sequenza_cerchio = sequenza_c.fetchall() 
sequenza_i = cur.execute(f"SELECT Sequenza FROM movimenti WHERE Tasto = ?", ("i", )) 
sequenza_integrale = sequenza_i.fetchall() 
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
            
            
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
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
        
    return render_template("index.html", user = current_user.id)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, use_reloader = False)



