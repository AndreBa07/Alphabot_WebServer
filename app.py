from flask import Flask, request, render_template
import AlphaBot

larry = AlphaBot.AlphaBot()
larry.stop()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
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
    elif request.method == "GET":
        
    render_template("./templates/index.html")
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
