from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename
import os
from routes import api
from llm_handler import get_llm_response

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Register blueprint
app.register_blueprint(api)

UPLOAD_FOLDER = "uploads/"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

chat_history = []
users = {}

@app.route("/")
def home():
    if not session.get("logged_in"):
        return redirect(url_for("auth"))
    return render_template("index.html", history=chat_history)

@app.route("/clear", methods=["POST"])
def clear_chat():
    global chat_history
    chat_history = []
    return redirect("/")

@app.route("/auth", methods=["GET", "POST"])
def auth():
    if request.method == "GET":
        return render_template("login.html")
    
    email = request.form.get("email")
    password = request.form.get("password")
    mode = request.form.get("mode")

    if not email or not password:
        return render_template("login.html", error="Email and password required.")

    if mode == "signup":
        if email in users:
            return render_template("login.html", error="User already exists.")
        users[email] = password
        session["logged_in"] = True
        return redirect(url_for("home"))
    
    elif mode == "login":
        if users.get(email) == password:
            session["logged_in"] = True
            return redirect(url_for("home"))
        return render_template("login.html", error="Invalid credentials.")
    
    return render_template("login.html", error="Invalid mode.")

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("auth"))

if __name__ == "__main__":
    app.run(debug=True)