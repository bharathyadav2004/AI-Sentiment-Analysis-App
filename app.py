from flask import Flask, render_template, request, jsonify
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import sqlite3

nltk.download('vader_lexicon')

app = Flask(__name__)

# Initialize the Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Set up SQLite database
def init_db():
    conn = sqlite3.connect('sentiment_analysis.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()
    text = data['text']
    
    # Analyze sentiment
    sentiment = sia.polarity_scores(text)
    
    # Determine if sentiment is positive, neutral, or negative
    if sentiment['compound'] >= 0.05:
        result = 'Positive'
    elif sentiment['compound'] <= -0.05:
        result = 'Negative'
    else:
        result = 'Neutral'
    
    # Store in database
    conn = sqlite3.connect('sentiment_analysis.db')
    c = conn.cursor()
    c.execute('INSERT INTO history (text, sentiment) VALUES (?, ?)', (text, result))
    conn.commit()
    conn.close()
    
    return jsonify({'sentiment': result})

if __name__ == '__main__':
    init_db()  # Initialize the database when the app starts
    app.run(debug=True)
