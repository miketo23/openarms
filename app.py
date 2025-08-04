from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


# Initialize SQLite database
def init_db():
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                amount REAL
            )
            '''
        )
        conn.commit()
init_db()

# Initialize a counter
form_count = 0

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/donate', methods=['POST'])
def donate():
    global form_count
    data = request.json
    name = data['name']
    email = data['email']
    amount = data['amount']

    # Insert into SQLite database
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (name, email, amount) VALUES (?, ?, ?)',
            (name, email, amount)
        )
        conn.commit()

    form_count += 1

    # Process data and respond with JSON
    response = {
        'message': 'Form submitted successfully!',
        'form_count': form_count,
        'success': True
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/map')
def contact():
    return render_template('contact.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')


@app.route('/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, email, amount FROM users')
    users = cursor.fetchall()
    conn.close()
    user_list = [{'name': user[0], 'email': user[1], 'amount': user[2]} for user in users]
    return jsonify(user_list)

if __name__ == '__main__':
    app.run(debug=True)
