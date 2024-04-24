from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Connect to SQLite database
def get_db():
    conn = sqlite3.connect('scales.db')  # Connects to the SQLite database
    conn.row_factory = sqlite3.Row  # Makes returned rows accessible as dictionaries
    return conn

# Create tables for scales and users if they don't exist
with get_db() as db:
    db.execute('''CREATE TABLE IF NOT EXISTS scales (
                  scale_number INTEGER PRIMARY KEY,
                  points INTEGER DEFAULT 0
                  )''')

    db.execute('''CREATE TABLE IF NOT EXISTS users (
                  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  points INTEGER DEFAULT 0
                  )''')

# Endpoint to get the points for a specific scale
@app.route('/scales/<int:scale_number>', methods=['GET'])
def get_scale_points(scale_number):
    with get_db() as db:
        row = db.execute("SELECT points FROM scales WHERE scale_number = ?", (scale_number,)).fetchone()
        points = row['points'] if row else 0
        return jsonify({'scale_number': scale_number, 'points': points})

# Endpoint to add points to a specific scale
@app.route('/add-points', methods=['POST'])
def add_points():
    data = request.json
    scale_number = data.get('scale_number')
    additional_points = data.get('points', 0)

    if not scale_number or additional_points <= 0:
        return jsonify({'error': 'Invalid input'}), 400

    with get_db() as db:
        # Check if the scale exists
        row = db.execute("SELECT points FROM scales WHERE scale_number = ?", (scale_number,)).fetchone()
        current_points = row['points'] if row else 0
        new_points = current_points + additional_points

        if row:
            db.execute("UPDATE scales SET points = ? WHERE scale_number = ?", (new_points, scale_number))
        else:
            db.execute("INSERT INTO scales (scale_number, points) VALUES (?, ?)", (scale_number, new_points))

    return jsonify({'scale_number': scale_number, 'points': new_points})

# Endpoint to get or create a user by name
@app.route('/user', methods=['POST'])
def get_or_create_user():
    data = request.json
    name = data.get('name')

    if not name:
        return jsonify({'error': 'Name is required'}), 400

    with get_db() as db:
        # Check if the user already exists
        row = db.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchone()

        if row:
            return jsonify({'user_id': row['user_id'], 'name': row['name'], 'points': row['points']})
        else:
            db.execute("INSERT INTO users (name) VALUES (?)", (name,))
            new_row = db.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchone()
            return jsonify({'user_id': new_row['user_id'], 'name': new_row['name'], 'points': new_row['points']})

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)  # Runs the Flask server in debug mode for development