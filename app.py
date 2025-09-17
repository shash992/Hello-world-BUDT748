from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'user_management')

mysql = MySQL(app)

@app.route('/user', methods=['POST'])
def add_user():
    if request.is_json:
        data = request.get_json() # Get data as JSON
        name = data['name']
        email = data['email']
        cur = mysql.connection.cursor()
        # SQL query string
        sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
        # Execute the SQL command
        cur.execute(sql, (name, email))
        # Commit the changes in the database
        mysql.connection.commit()
        # Close the cursor
        cur.close()
        # Insert into database or process data here
        return jsonify(message="User added successfully"), 201
    else:
        return jsonify(error="Error in submission"), 400

@app.route('/users', methods=['GET'])
def get_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, email FROM users") # Ensure thefields match what's expected in the frontend
    users = cur.fetchall()
    cur.close()
# Convert query results to a list of dicts to jsonify them easily
    user_dicts = [{'id': user[0], 'name': user[1], 'email': user[2]} for user in users]
    return jsonify(user_dicts)

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    return jsonify(message="User deleted successfully")

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app. run (debug=True)