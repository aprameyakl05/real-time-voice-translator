from flask import Flask, request, jsonify, render_template
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

main = Flask(__name__)

# Database connection
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Aneesh@12345',
    port='3306',
    database='user'  # Database name
)
mycursor = mydb.cursor()

# Route for user registration
@main.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm-password']

    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    # Hash the password for security
    hashed_password = generate_password_hash(password)

    try:
        # Update the table name to translogin
        mycursor.execute("INSERT INTO translogin (name, email, password) VALUES (%s, %s, %s)", (name,email,hashed_password))

        mydb.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except mysql.connector.Error as err:
        if err.errno == 1062:  # Duplicate entry error
            return jsonify({"error": "Email already exists"}), 400
        return jsonify({"error": str(err)}), 500

# Route for user login
@main.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    # Update the table name to translogin
    mycursor.execute("SELECT * FROM translogin WHERE email = %s", (email,))
    user = mycursor.fetchone()

    if user and check_password_hash(user[3], password):  # user[3] is the password column
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401

if __name__ == '__main__':
    main.run(debug=True)