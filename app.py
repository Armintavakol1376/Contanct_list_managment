from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)  # Ensure 'app' is defined

CONTACTS_FILE = "contacts.json"

def load_contacts():
    try:
        with open(CONTACTS_FILE, "r") as f:
            data = json.load(f)
            return data.get("contacts", [])
    except FileNotFoundError:
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
    return jsonify(contacts)

@app.route("/add_contact", methods=["POST"])
def add_contact():
    data = request.json
    contacts = load_contacts()
    
    new_contact = {
        "name": data["name"],
        "age": data["age"],
        "email": data["email"]
    }
    
    contacts.append(new_contact)
    save_contacts(contacts)
    
    return jsonify({"message": "Contact added successfully!", "contacts": contacts})

@app.route("/delete_contact/<int:index>", methods=["DELETE"])
def delete_contact(index):
    contacts = load_contacts()
    if 0 <= index < len(contacts):
        contacts.pop(index)
        save_contacts(contacts)
        return jsonify({"message": "Contact deleted successfully!", "contacts": contacts})
    return jsonify({"error": "Invalid index"}), 400

if __name__ == "__main__":
    app.run(debug=True)  # This must be at the end
