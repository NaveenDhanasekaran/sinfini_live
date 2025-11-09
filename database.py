import sqlite3
import os
from werkzeug.security import generate_password_hash

DATABASE_PATH = 'sinfin_database.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Blog posts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blog_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT DEFAULT 'Admin',
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Gallery items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gallery_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            media_type TEXT NOT NULL,
            media_url TEXT NOT NULL,
            title TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Chatbot settings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chatbot_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            greeting TEXT DEFAULT 'Hello! How can I help you today?',
            faqs TEXT DEFAULT '[]',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Check if default admin user exists
    cursor.execute('SELECT * FROM users WHERE username = ?', ('ayeshanawazraza@gmail.com',))
    if not cursor.fetchone():
        password_hash = generate_password_hash('Emotional.Intelligence@123')
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', 
                      ('ayeshanawazraza@gmail.com', password_hash))
    
    # Also keep the old admin for backward compatibility
    cursor.execute('SELECT * FROM users WHERE username = ?', ('admin',))
    if not cursor.fetchone():
        password_hash = generate_password_hash('admin123')
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', 
                      ('admin', password_hash))
    
    # Check if chatbot settings exist
    cursor.execute('SELECT * FROM chatbot_settings')
    if not cursor.fetchone():
        default_faqs = '''[
            {
                "question": "What products do you offer?",
                "answer": "We specialize in premium cotton and synthetic ladies' fabrics, garments, linens, and terry toweling products.",
                "keywords": ["products", "offer", "sell", "fabrics", "textile"]
            },
            {
                "question": "Where do you export to?",
                "answer": "We export to international markets across Asia, Africa, and Europe.",
                "keywords": ["export", "ship", "countries", "where", "location"]
            },
            {
                "question": "How can I contact you?",
                "answer": "You can reach us through our contact form or email us at info@sinfinimarketing.com. We are located in Sharjah, UAE.",
                "keywords": ["contact", "email", "phone", "reach", "address"]
            },
            {
                "question": "What is your company's specialty?",
                "answer": "Sinfini Marketing FZC specializes in exporting premium quality textiles including cotton and synthetic fabrics, garments, linens, and terry toweling products.",
                "keywords": ["specialty", "specialize", "focus", "expertise"]
            }
        ]'''
        cursor.execute('INSERT INTO chatbot_settings (greeting, faqs) VALUES (?, ?)', 
                      ('Hello! Welcome to Sinfini Marketing FZC. How can I assist you today?', default_faqs))
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
