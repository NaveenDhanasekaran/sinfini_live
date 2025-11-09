from datetime import datetime

class User:
    @staticmethod
    def get_by_id(db, user_id):
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    @staticmethod
    def get_by_username(db, username):
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        return dict(row) if row else None

class Product:
    @staticmethod
    def get_all(db):
        cursor = db.cursor()
        cursor.execute('SELECT * FROM products ORDER BY created_at DESC')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    @staticmethod
    def get_by_id(db, product_id):
        cursor = db.cursor()
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    @staticmethod
    def create(db, name, category, description, image_url=None):
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO products (name, category, description, image_url)
            VALUES (?, ?, ?, ?)
        ''', (name, category, description, image_url))
        db.commit()
        return cursor.lastrowid
    
    @staticmethod
    def update(db, product_id, name, category, description, image_url):
        cursor = db.cursor()
        cursor.execute('''
            UPDATE products 
            SET name = ?, category = ?, description = ?, image_url = ?, 
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (name, category, description, image_url, product_id))
        db.commit()
    
    @staticmethod
    def delete(db, product_id):
        cursor = db.cursor()
        cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
        db.commit()

class BlogPost:
    @staticmethod
    def get_all(db):
        cursor = db.cursor()
        cursor.execute('SELECT * FROM blog_posts ORDER BY created_at DESC')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    @staticmethod
    def get_by_id(db, post_id):
        cursor = db.cursor()
        cursor.execute('SELECT * FROM blog_posts WHERE id = ?', (post_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    @staticmethod
    def create(db, title, content, author='Admin', image_url=None):
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO blog_posts (title, content, author, image_url)
            VALUES (?, ?, ?, ?)
        ''', (title, content, author, image_url))
        db.commit()
        return cursor.lastrowid
    
    @staticmethod
    def update(db, post_id, title, content, author, image_url):
        cursor = db.cursor()
        cursor.execute('''
            UPDATE blog_posts 
            SET title = ?, content = ?, author = ?, image_url = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (title, content, author, image_url, post_id))
        db.commit()
    
    @staticmethod
    def delete(db, post_id):
        cursor = db.cursor()
        cursor.execute('DELETE FROM blog_posts WHERE id = ?', (post_id,))
        db.commit()

class GalleryItem:
    @staticmethod
    def get_all(db):
        cursor = db.cursor()
        cursor.execute('SELECT * FROM gallery_items ORDER BY created_at DESC')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    @staticmethod
    def get_by_id(db, item_id):
        cursor = db.cursor()
        cursor.execute('SELECT * FROM gallery_items WHERE id = ?', (item_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    @staticmethod
    def create(db, media_type, media_url, title='', description=''):
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO gallery_items (media_type, media_url, title, description)
            VALUES (?, ?, ?, ?)
        ''', (media_type, media_url, title, description))
        db.commit()
        return cursor.lastrowid
    
    @staticmethod
    def delete(db, item_id):
        cursor = db.cursor()
        cursor.execute('DELETE FROM gallery_items WHERE id = ?', (item_id,))
        db.commit()

class ChatbotSettings:
    @staticmethod
    def get(db):
        cursor = db.cursor()
        cursor.execute('SELECT * FROM chatbot_settings LIMIT 1')
        row = cursor.fetchone()
        return dict(row) if row else {'greeting': 'Hello!', 'faqs': '[]'}
    
    @staticmethod
    def update(db, greeting, faqs):
        cursor = db.cursor()
        cursor.execute('''
            UPDATE chatbot_settings 
            SET greeting = ?, faqs = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = 1
        ''', (greeting, faqs))
        db.commit()
