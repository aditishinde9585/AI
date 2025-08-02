from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename
import os
from routes import api
from llm_handler import get_llm_response

app = Flask(name)
app.secret_key = "your_secret_key"

# Register blueprint
app.register_blueprint(api)

# Upload folder setup
UPLOAD_FOLDER = "uploads/"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

chat_history = []
users = {}  # In-memory user store

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

# Required for Render or cloud deployment (host="0.0.0.0", port from env)
if name == "main":
    port = int(os.environ.get("PORT", 5000))  # PORT environment variable on Render
    app.run(host="0.0.0.0", port=port, debug=True)