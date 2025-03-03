# Contact List Management System 📇

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/flask-2.3.x-green)
![MySQL](https://img.shields.io/badge/mysql-8.0%2B-orange)
![License](https://img.shields.io/badge/license-MIT-brightgreen)

A robust Flask-based web application for managing contacts with MySQL integration, JWT authentication, and granular role-based access control (RBAC).

![Screenshot](screenshot.png) <!-- Add actual screenshot later -->

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Technologies](#technologies)
- [License](#license)
- [Contributing](#contributing)

## Features ✨
- 🔐 **Secure Authentication**  
  JWT-based login/registration using Flask-JWT-Extended
- 👮 **Role-Based Access Control**
  - **Admin**: Full CRUD operations + user management
  - **Manager**: Create, update, and view contacts
  - **User**: View and search contacts
- 🔍 **Advanced Contact Management**
  - Add/edit/delete contacts with validation
  - Real-time search across all fields
  - Pagination support (future implementation)
- 🗄️ **Reliable Data Storage**  
  MySQL integration with Flask-SQLAlchemy ORM

## Prerequisites 📋
- Python 3.8+
- MySQL Server 8.0+
- pip package manager

## Installation 🛠️

### 1. Clone Repository
```bash
git clone https://github.com/Armintavakol1376/Contanct_list_managment.git
cd Contanct_list_managment

2. Create Virtual Environment
bash
Copy
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
bash
Copy
pip install -r requirements.txt

Configuration ⚙️
1. MySQL Setup
bash
Copy
sudo apt update
sudo apt install mysql-server libmysqlclient-dev

2. Database Configuration
sql
Copy
CREATE DATABASE flask_db;
CREATE USER 'armin'@'localhost' IDENTIFIED BY 'armin1376';
GRANT ALL PRIVILEGES ON flask_db.* TO 'armin'@'localhost';
FLUSH PRIVILEGES;

3. Initialize Database
bash
Copy
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
Usage 🚀
Running the Application

bash
Copy
export FLASK_APP=app.py
export FLASK_DEBUG=1  # Enable development mode
flask run
Visit http://localhost:5000 in your browser.

First-Time Setup
Register a user:

bash
Copy
curl -X POST -H "Content-Type: application/json" -d '{
  "email": "admin@example.com",
  "password": "admin123",
  "role": "admin"
}' http://localhost:5000/register
Login to get JWT token:

bash
Copy
curl -X POST -H "Content-Type: application/json" -d '{
  "email": "admin@example.com",
  "password": "admin123"
}' http://localhost:5000/login

API Endpoints 🔌
Method	Endpoint	Description	Access Level
POST	/register	Register new user	Public
POST	/login	User authentication	Public
POST	/add_contact	Add new contact	User+
GET	/get_contacts	Retrieve contacts	User+
PUT	/edit_contact/{id}	Update existing contact	Manager+
DELETE	/delete_contact/{id}	Remove contact	Admin

Technologies 🛠
Backend:
Flask
SQLAlchemy
JWT

Frontend:
HTML5
JavaScript

Database:
MySQL

Tools:
Git

License 📄
This project is licensed under the MIT License - see the LICENSE file for details.

Contributing 🤝
Contributions are welcome! Please follow these steps:

Fork the repository

Create your feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add some amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request
