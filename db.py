# db.py

import sqlite3

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

def insert_sentiment(text, sentiment):
    conn = sqlite3.connect('sentiment_analysis.db')
    c = conn.cursor()
    c.execute('INSERT INTO history (text, sentiment) VALUES (?, ?)', (text, sentiment))
    conn.commit()
    conn.close()
