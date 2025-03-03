# Contact List Management System 📇

A Flask-based web application for managing contacts with MySQL integration, JWT authentication, and role-based access control (RBAC).


## Features
- 🔐 **JWT Authentication**: Secure login/registration with Flask-JWT-Extended.
- 👥 **Role-Based Access Control**: 
  - **Admin**: Full access (add/edit/delete contacts).
  - **Manager**: Add/edit contacts.
  - **User**: View and search contacts.
- 📞 **Contact Management**: 
  - Add, edit, delete, and search contacts.
  - Real-time search functionality.
- 🗃️ **MySQL Integration**: Persistent data storage.

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Armintavakol1376/Contanct_list_managment.git
   cd Contanct_list_managment
2.set up a virtual environment:

python3 -m venv venv
source venv/bin/activate

3.Install dependencies:
pip install -r requirements.txt

4.configure MYSQL:
#Install MYSQL on ubuntu:
sudo apt install mysql-server libmysqlclienct-dev

Create a database and user(match app.py settings):
CREATE DATABASE flask_db;
CREATE USER 'armin'@'localhost' IDENTIFIED BY 'armin1376';
GRANT ALL PRIVILEGES ON flask_db.* TO 'armin'@'localhost';
FLUSH PRIVILEGES;

5.Initialize the database:
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()

6.Run the app:
export FLASK_APP=app.py
flask run
#Visit http://localhost:5000.



