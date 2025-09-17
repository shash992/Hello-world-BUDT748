from flask import Flask, request, jsonify, render_template, abort, redirect
from flask_mysqldb import MySQL
from flask_mysqldb import MySQLdb
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = 'user_management'
mysql = MySQL(app)

# --- Flask-Login Config ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def is_admin():
    return current_user.role in ['Admin']

def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles:
                return abort(403)
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

class User(UserMixin):
    def __init__(self, id, name, email, password, role):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user_data = cur.fetchone()
    cur.close()
    if user_data:
        return User(*user_data)
    return None

# --- Login ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user_data = cur.fetchone()
        cur.close()

        # user_data: (id, name, email, password_hash, role)
        if user_data and check_password_hash(user_data[3], password):
            user = User(*user_data)
            login_user(user)
            return redirect('/')
        else:
            return render_template('login.html', error="Invalid credentials")
    # GET -> just render the form
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

# --- Add User (Admin Only) ---
@app.route('/user', methods=['POST'])
@login_required
@role_required('Admin')
def add_user():
    if request.is_json:
        data = request.get_json()
        name = data['name']
        email = data['email']
        role = data.get('role', 'Admin')
        password = generate_password_hash(data.get('password', 'test123'))
        cur = mysql.connection.cursor()
        sql = "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s,%s)"
        cur.execute(sql, (name, email, password, role))
        mysql.connection.commit()
        cur.close()
        return jsonify(message="User added successfully"), 201
    return jsonify(error="Invalid submission"), 400

@app.route('/users', methods=['GET'])
@login_required
def get_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, email, role FROM users")
    users = cur.fetchall()
    cur.close()
    user_dicts = []
    for user in users:
        user_data = {
            'id': user[0],
            'name': user[1],
            'role': user[3]
        }
    # Admins can view emails, customers can't
        if is_admin():
            user_data['email'] = user[2]
        user_dicts.append(user_data)
    return jsonify(user_dicts)

# --- Delete User (Admin Only) ---
@app.route('/user/<int:id>', methods=['DELETE'])
@login_required
@role_required('Admin')
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    return jsonify(message="User deleted successfully")

# --- Home Page ---
@app.route('/')
@login_required
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)