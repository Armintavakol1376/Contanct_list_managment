from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

CONTACTS_FILE = "contacts.json"

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

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_contacts", methods=["GET"])
def get_contacts():
    contacts = load_contacts()
    return jsonify({"contacts": contacts})

@app.route("/add_contact", methods=["POST"])
def add_contact():
    data = request.json
    contacts = load_contacts()

    new_contact = {
        "name": data["name"],
        "age": data["age"],
        "email": data["email"]
    }

    if any(contact["email"] == new_contact["email"] for contact in contacts):
        return jsonify({"error": "Contact with this email already exists."}), 400

    contacts.append(new_contact)
    save_contacts(contacts)
    
    return jsonify({"message": "Contact added successfully.", "contacts": contacts})

@app.route("/delete_contact/<int:index>", methods=["DELETE"])
def delete_contact(index):
    contacts = load_contacts()

    if index < 0 or index >= len(contacts):
        return jsonify({"error": "Invalid index"}), 400

    contacts.pop(index)
    save_contacts(contacts)
    
    return jsonify({"message": "Contact deleted successfully.", "contacts": contacts})

@app.route("/search_contacts/<name>", methods=["GET"])
def search_contacts(name):
    contacts = load_contacts()
    filtered = [c for c in contacts if name.lower() in c["name"].lower()]
    return jsonify({"contacts": filtered})

if __name__ == "__main__":
    app.run(debug=True)
