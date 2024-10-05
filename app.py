# app.py

from flask import Flask, render_template, request, jsonify
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from db import init_db, insert_sentiment  # Import the functions from db.py

nltk.download('vader_lexicon')

app = Flask(__name__)

# Initialize the Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

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
    
    # Store in database using the function from db.py
    insert_sentiment(text, result)
    
    return jsonify({'sentiment': result})

if __name__ == '__main__':
    init_db()  # Initialize the database when the app starts
    app.run(debug=True)
