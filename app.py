from flask import Flask, render_template, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required,
    get_jwt_identity, verify_jwt_in_request, get_jwt
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from functools import wraps

app = Flask(__name__)

# 🔹 Configurations
app.config["JWT_SECRET_KEY"] = "supersecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://armin:armin1376@localhost/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# 🔹 Define User & Contact Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user")

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    added_by = db.Column(db.String(100), db.ForeignKey('user.email'), nullable=False)

# 🔹 Role-Based Access Control (RBAC) Decorator
def role_required(allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()  # Ensure JWT is valid
            # get_jwt_identity() now returns a string (user's email)
            current_user_email = get_jwt_identity()
            # Retrieve additional claims from the token
            current_user_role = get_jwt().get("role")
            # Fetch user role from DB to double-check permissions
            user = User.query.filter_by(email=current_user_email).first()
            if not user or user.role not in allowed_roles:
                return jsonify({"error": "Unauthorized - Insufficient Permissions"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

# 🔹 Route for Login Page (GET renders the form)
@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

# 🔹 Route for User Login (Authenticate & Generate Token)
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email, password=password).first()
    if user:
        # Use a string (e.g., email) as identity and pass role as an additional claim
        access_token = create_access_token(identity=email, additional_claims={"role": user.role})
        return jsonify({"token": access_token, "role": user.role})
    
    return jsonify({"error": "Invalid credentials"}), 401

# 🔹 Route for Contact Management Page (Protected)
@app.route("/")
def home():
    return render_template("index.html")

# 🔹 Register User & Store in MySQL
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    new_user = User(email=email, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

# 🔹 Add Contact & Store in MySQL (Protected)
@app.route("/add_contact", methods=["POST"])
@jwt_required()
@role_required(["admin", "manager", "user"])
def add_contact():
    current_user_email = get_jwt_identity()
    data = request.json
    name = data.get("name")
    age = data.get("age")
    email = data.get("email")
    if not name or not age or not email:
        return jsonify({"error": "All fields are required"}), 400

    new_contact = Contact(name=name, age=age, email=email, added_by=current_user_email)
    db.session.add(new_contact)
    db.session.commit()
    return jsonify({"success": True, "message": "Contact added successfully"}), 201

# 🔹 Get Contacts (Protected)
@app.route("/get_contacts", methods=["GET"])
@jwt_required()
def get_contacts():
    current_user_email = get_jwt_identity()
    # Get the search query from the URL, default to empty string if not provided
    search_query = request.args.get("q", "").strip()
    
    # Start with contacts for the current user
    contacts_query = Contact.query.filter_by(added_by=current_user_email)
    
    # If a search query is provided, filter by name or email
    if search_query:
        contacts_query = contacts_query.filter(
            (Contact.name.like(f"%{search_query}%")) | (Contact.email.like(f"%{search_query}%"))
        )
    
    contacts = contacts_query.all()
    result = [{"id": c.id, "name": c.name, "age": c.age, "email": c.email, "added_by": c.added_by} for c in contacts]
    return jsonify({"contacts": result}), 200


# 🔹 Delete Contact (Only Admin)
@app.route("/delete_contact/<int:id>", methods=["DELETE"])
@jwt_required()
@role_required(["admin"])
def delete_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({"error": "Contact not found"}), 404
    db.session.delete(contact)
    db.session.commit()
    return jsonify({"message": "Contact deleted successfully"}), 200

# 🔹 Edit Contact (Only Admin & Manager)
@app.route("/edit_contact/<int:id>", methods=["PUT"])
@jwt_required()
@role_required(["admin", "manager"])
def edit_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({"error": "Contact not found"}), 404
    data = request.json
    contact.name = data.get("name", contact.name)
    contact.age = data.get("age", contact.age)
    contact.email = data.get("email", contact.email)
    db.session.commit()
    return jsonify({"message": "Contact updated successfully"}), 200

# 🔹 Log Incoming Requests
@app.before_request
def log_request():
    print(f"Incoming request: {request.method} {request.path}")

if __name__ == "__main__":
    app.run(debug=True)
