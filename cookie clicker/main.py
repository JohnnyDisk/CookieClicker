from flask import Flask, render_template, request, jsonify
import time
import sqlite3
from better_profanity import profanity

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('click_data.db')
    c = conn.cursor()
    # Drop the existing clicks table if it exists
    c.execute("DROP TABLE IF EXISTS clicks")
    c.execute('''CREATE TABLE IF NOT EXISTS clicks (username TEXT, count INTEGER, timestamp REAL, highest_cps INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS game_state (username TEXT, active INTEGER)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    username = request.json.get('username')
    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    # Check for profanity
    if profanity.contains_profanity(username):
        return jsonify({"error": "Username contains profanity"}), 400

    start_time = time.time()
    
    # Set the game state to active
    conn = sqlite3.connect('click_data.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO game_state (username, active) VALUES (?, ?)", (username, 1))
    conn.commit()
    conn.close()
    
    return jsonify({"start_time": start_time, "username": username})

@app.route('/count_clicks', methods=['POST'])
def count_clicks():
    username = request.json.get('username')
    
    # Check if the game is active for the user
    conn = sqlite3.connect('click_data.db')
    c = conn.cursor()
    c.execute("SELECT active FROM game_state WHERE username = ?", (username,))
    game_active = c.fetchone()
    
    if not game_active or game_active[0] == 0:
        return jsonify({"error": "Game is not active. Cannot count clicks."}), 400
    
    # Increment the click count without rate limiting
    current_time = time.time()
    c.execute("INSERT INTO clicks (username, count, timestamp) VALUES (?, ?, ?)", (username, 1, current_time))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success"})

@app.route('/save_click_data', methods=['POST'])
def save_click_data():
    username = request.json.get('username')
    count = request.json.get('count')
    highest_cps = request.json.get('highestCps')

    # Log the incoming data
    print(f"Received data - Username: {username}, Count: {count}, Highest CPS: {highest_cps}")

    # Check for profanity
    if profanity.contains_profanity(username):
        return jsonify({"error": "Username contains profanity"}), 400

    # Check if the game is active for the user
    conn = sqlite3.connect('click_data.db')
    c = conn.cursor()
    c.execute("SELECT active FROM game_state WHERE username = ?", (username,))
    game_active = c.fetchone()
    
    if not game_active or game_active[0] == 0:
        return jsonify({"error": "Game is not active. Cannot save click data."}), 400
    
    if not username:
        return jsonify({"error": "Username is required"}), 400
    timestamp = time.time()
    
    c.execute("INSERT INTO clicks (username, count, timestamp, highest_cps) VALUES (?, ?, ?, ?)", (username, count, timestamp, highest_cps))
    conn.commit()
    
    # Set the game state to inactive after saving
    c.execute("UPDATE game_state SET active = 0 WHERE username = ?", (username,))
    conn.commit()

    return jsonify({"status": "success"})  # Added return statement

@app.route('/leaderboard')
def leaderboard():
    conn = sqlite3.connect('click_data.db')
    c = conn.cursor()
    c.execute("SELECT username, SUM(count) as total_clicks, MAX(highest_cps) as highest_cps FROM clicks GROUP BY username HAVING total_clicks <= 600 ORDER BY total_clicks DESC")
    results = c.fetchall()
    conn.close()
    return render_template('leaderboard.html', results=results)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
