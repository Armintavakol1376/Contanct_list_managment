from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import json
import os

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "supersecretkey"
jwt = JWTManager(app)

USERS_FILE = "users.json"
CONTACTS_FILE = "contacts.json"

# Load & Save Users
def load_users():
    if not os.path.exists(USERS_FILE):
        save_users({})
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# Load & Save Contacts
def load_contacts():
    if not os.path.exists(CONTACTS_FILE):
        save_contacts([])
    try:
        with open(CONTACTS_FILE, "r") as f:
            data = json.load(f)
            return data.get("contacts", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as f:
        json.dump({"contacts": contacts}, f, indent=4)

# 🔹 Route for Login Page
@app.route("/login")
def login_page():
    return render_template("login.html")

# 🔹 Route for Contact Management Page (Protected)
@app.route("/")
def home():
    return render_template("index.html")

# 🔹 User Registration
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    users = load_users()

    if data["email"] in users:
        return jsonify({"error": "User already exists"}), 400

    users[data["email"]] = {"password": data["password"]}
    save_users(users)

    return jsonify({"message": "User registered successfully"}), 201

# 🔹 User Login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    users = load_users()

    #  Prevent blank email or password login
    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password are required"}), 400

    if data["email"] in users and users[data["email"]]["password"] == data["password"]:
        access_token = create_access_token(identity=data["email"])
        return jsonify({"token": access_token})

    return jsonify({"error": "Invalid credentials"}), 401

if __name__ == "__main__":
    app.run(debug=True)

