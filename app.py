from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

# Initialize the Flask application
app = Flask(__name__)

# Configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'  # Your MySQL host (usually localhost)
app.config['MYSQL_USER'] = 'root'       # Your MySQL username
app.config['MYSQL_PASSWORD'] = '****'  # Your MySQL password
app.config['MYSQL_DB'] = 'flask_crud'    # The database you're using

# Initialize MySQL
mysql = MySQL(app)

# Route to display all users
@app.route('/')
def index():
    cur = mysql.connection.cursor()  # Create a cursor to interact with the DB
    cur.execute("SELECT * FROM users")  # SQL query to get all users
    users = cur.fetchall()  # Fetch all results from the query
    return render_template('index.html', users=users)  # Pass users to template

# Route to create a new user
@app.route('/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':  # Check if the request is POST (form submission)
        name = request.form['name']  # Get the 'name' from the form
        email = request.form['email']  # Get the 'email' from the form
        cur = mysql.connection.cursor()  # Create cursor
        cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))  # Insert user into DB
        mysql.connection.commit()  # Commit the changes to the database
        return redirect(url_for('index'))  # Redirect to index page
    return render_template('create.html')  # Render the form template

# Route to update an existing user's information
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (id,))  # Get user by ID
    user = cur.fetchone()  # Fetch a single result

    if request.method == 'POST':  # Handle POST request (form submission)
        name = request.form['name']
        email = request.form['email']
        cur.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, id))  # Update the DB
        mysql.connection.commit()  # Commit changes
        return redirect(url_for('index'))  # Redirect to index page
    
    return render_template('update.html', user=user)  # Render the update form with user data

# Route to delete a user
@app.route('/delete/<int:id>', methods=['GET'])
def delete_user(id):
    cur = mysql.connection.cursor()  # Create cursor
    cur.execute("DELETE FROM users WHERE id = %s", (id,))  # Delete user by ID
    mysql.connection.commit()  # Commit the change
    return redirect(url_for('index'))  # Redirect to the index page

# Run the application
if __name__ == "__main__":
    app.run(debug=True)


