from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app) 

def get_db_connection():
    conn = sqlite3.connect('votes.db')
    conn.row_factory = sqlite3.Row  
    return conn

@app.route('/submit_vote', methods=['POST'])
def submit_vote():
    candidate = request.json['candidate']
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO votes (candidate) VALUES (?)', (candidate,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"Vote for {candidate} submitted successfully!"})


@app.route('/results')
def results():
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT candidate, COUNT(*) as vote_count FROM votes GROUP BY candidate')
        vote_counts = c.fetchall()
        conn.close()

        return jsonify({'vote_counts': [{'candidate': row['candidate'], 'vote_count': row['vote_count']} for row in vote_counts]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000,ssl_context=('cert.pem', 'key.pem'))  #
