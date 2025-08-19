import sqlite3
import string
import random
from datetime import datetime

def generate_short_code(length=6):
    """Generates a random short code for the URL."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def init_db():
    """Initializes the database and creates the table if it doesn't exist."""
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_url(original_url, short_code=None):
    """
    Adds a new URL to the database.
    If no short code is provided, generates a random one.
    Returns the short code on success, None on failure.
    """
    if short_code is None:
        short_code = generate_short_code()

    conn = sqlite3.connect('urls.db')
    c = conn.cursor()

    try:
        c.execute('INSERT INTO urls (original_url, short_code) VALUES (?, ?)',
                  (original_url, short_code))
        conn.commit()
        return short_code
    except sqlite3.IntegrityError:
        # Handle duplicate short codes by trying again with a new code
        return add_url(original_url)
    finally:
        conn.close()

def get_original_url(short_code):
    """Retrieves the original URL for a given short code."""
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute('SELECT original_url FROM urls WHERE short_code = ?', (short_code,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None
