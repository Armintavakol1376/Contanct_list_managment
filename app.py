from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)

# 🔹 MySQL Database Configuration (Keep this only once)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://flask_user:your_password@localhost/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'supersecretkey'

db = SQLAlchemy(app)
jwt = JWTManager(app)

# 🔹 Define User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'superuser', 'user'

# 🔹 Define Contact Model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    added_by = db.Column(db.String(100), db.ForeignKey('user.email'), nullable=False)

# 🔹 Create Database Tables
with app.app_context():
    db.create_all()

# 🔹 Middleware for Role-Based Access Control
def role_required(required_role):
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            user = User.query.filter_by(email=current_user).first()
            if not user or user.role != required_role:
                return jsonify({"error": "Unauthorized access"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator

# 🔹 User Registration
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    existing_user = User.query.filter_by(email=data["email"]).first()

    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(data["password"], method="pbkdf2:sha256")
    new_user = User(email=data["email"], password=hashed_password, role=data["role"])
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

# 🔹 User Login with JWT
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()

    if user and check_password_hash(user.password, data["password"]):
        access_token = create_access_token(identity=user.email)
        return jsonify({"token": access_token}), 200

    return jsonify({"error": "Invalid credentials"}), 401

# 🔹 Add a Contact (Only Authenticated Users)
@app.route("/add_contact", methods=["POST"])
@jwt_required()
def add_contact():
    current_user_email = get_jwt_identity()
    data = request.json

    if not data.get("name") or not data.get("age") or not data.get("email"):
        return jsonify({"error": "All fields are required"}), 400

    new_contact = Contact(
        name=data["name"], age=data["age"], email=data["email"], added_by=current_user_email
    )
    
    db.session.add(new_contact)
    db.session.commit()

    return jsonify({"message": "Contact added successfully!"}), 201

# 🔹 Admin-Only Endpoint
@app.route("/admin_dashboard", methods=["GET"])
@role_required("admin")
def admin_dashboard():
    return jsonify({"message": "Welcome, Admin!"})

# 🔹 Superuser-Only Endpoint
@app.route("/superuser_dashboard", methods=["GET"])
@role_required("superuser")
def superuser_dashboard():
    return jsonify({"message": "Welcome, Superuser!"})

# 🔹 Normal User-Only Endpoint
@app.route("/user_dashboard", methods=["GET"])
@role_required("user")
def user_dashboard():
    return jsonify({"message": "Welcome, User!"})

# 🔹 Home Route (Moved up)
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Flask App!"})

# 🔹 Test Connection to MySQL
with app.app_context():
    try:
        db.session.execute('SELECT 1')
        print("✅ Successfully connected to MySQL!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")

# 🔹 Run Flask App (Only once)
if __name__ == "__main__":
    app.run(debug=True)
