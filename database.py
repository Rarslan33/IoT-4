from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data.db')

def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                value TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        raise

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/resultater')
def resultater():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT timestamp, value FROM sensor_data ORDER BY timestamp DESC LIMIT 10')
    data = c.fetchall()
    conn.close()
    return render_template('resultater.html', data=data)

@app.route('/api/data', methods=['POST'])
def receive_data():
    try:
        data = request.get_data(as_text=True)
        if data:
            print(f"Modtaget rÃ¥ data: {data}")

            json_data = request.get_json()
            if json_data is None:
                return jsonify({"status": "error", "message": "Fejl i modtagelse af JSON data"}), 400

            message = json_data.get('message')
            if message:
                print(f"Modtaget besked: {message}")

                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                c.execute('INSERT INTO sensor_data (value) VALUES (?)', (message,))
                conn.commit()
                conn.close()

                return jsonify({"status": "success", "message": message})

            return jsonify({"status": "error", "message": "Ingen meddelelse fundet i data"}), 400
        else:
            return jsonify({"status": "error", "message": "Ingen data modtaget"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": f"Fejl ved modtagelse af data: {str(e)}"}), 400


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)