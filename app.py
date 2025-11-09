from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for, session, flash
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import timedelta
from database import init_db, get_db
from models import User, Product, BlogPost, GalleryItem, ChatbotSettings
import json
import subprocess
import atexit
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Email configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
SMTP_FROM_EMAIL = os.getenv('SMTP_FROM_EMAIL')
SMTP_FROM_NAME = os.getenv('SMTP_FROM_NAME', 'Sinfini Marketing FZC')

# Google Sheets configuration
GOOGLE_SHEETS_CREDENTIALS_FILE = os.getenv('GOOGLE_SHEETS_CREDENTIALS_FILE')
GOOGLE_SHEETS_SPREADSHEET_ID = os.getenv('GOOGLE_SHEETS_SPREADSHEET_ID')
GOOGLE_SHEETS_WORKSHEET_NAME = os.getenv('GOOGLE_SHEETS_WORKSHEET_NAME', 'Contact_Form_Submissions')
"""Ensure JWT is read from Authorization header to avoid 422 errors when verifying
tokens from the admin dashboard which sends `Authorization: Bearer <token>`.
"""
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'

CORS(app)
jwt = JWTManager(app)

# ---------- JWT error handlers for clearer behavior ----------
@jwt.unauthorized_loader
def _jwt_missing_token(err):
    # Missing Authorization header
    return jsonify({'error': 'missing_authorization', 'detail': err}), 401

@jwt.invalid_token_loader
def _jwt_invalid_token(err):
    # Invalid token format/signature
    return jsonify({'error': 'invalid_token', 'detail': err}), 401

@jwt.expired_token_loader
def _jwt_expired_token(jwt_header, jwt_payload):
    # Expired token
    return jsonify({'error': 'token_expired'}), 401

# ==================== WEB ROUTES (Flask Templates) ====================

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/products')
def products():
    return render_template('products.html')

# @app.route('/gallery')
# def gallery():
#     return render_template('gallery.html')

# @app.route('/blog')
# def blog():
#     return render_template('blog.html')

# @app.route('/blog/<int:post_id>')
# def blog_detail(post_id):
#     return render_template('blog_detail.html', post_id=post_id)

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Admin routes
@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin/dashboard.html')

@app.route('/admin/products')
def admin_products():
    return render_template('admin/products.html')

# @app.route('/admin/blog')
# def admin_blog():
#     return render_template('admin/blog.html')

# @app.route('/admin/gallery')
# def admin_gallery():
#     return render_template('admin/gallery.html')

@app.route('/admin/chatbot')
def admin_chatbot():
    return render_template('admin/chatbot.html')

# Ensure upload directories exist
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'products'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'blog'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'gallery'), exist_ok=True)

# Initialize database
init_db()

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4', 'webm', 'ogg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==================== AUTH ROUTES ====================

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = (data or {}).get('username')
        password = (data or {}).get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400

        # Dummy auth: accept any non-empty username/password
        access_token = create_access_token(identity=username)
        return jsonify({
            'access_token': access_token,
            'user': {
                'username': username
            }
        }), 200

    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/auth/verify', methods=['GET'])
@jwt_required()
def verify_token():
    identity = get_jwt_identity()
    return jsonify({'user': {'username': identity}}), 200

# ==================== PRODUCTS ROUTES ====================

@app.route('/api/products', methods=['GET'])
def get_products():
    db = get_db()
    products = Product.get_all(db)
    return jsonify(products), 200

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    db = get_db()
    product = Product.get_by_id(db, product_id)
    
    if product:
        return jsonify(product), 200
    
    return jsonify({'error': 'Product not found'}), 404

@app.route('/api/products', methods=['POST'])
@jwt_required()
def create_product():
    data = request.form
    image = request.files.get('image')
    
    image_url = None
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'products', filename)
        image.save(image_path)
        image_url = f'/uploads/products/{filename}'
    
    db = get_db()
    product_id = Product.create(
        db,
        name=data.get('name'),
        category=data.get('category'),
        description=data.get('description'),
        image_url=image_url
    )
    
    product = Product.get_by_id(db, product_id)
    return jsonify(product), 201

@app.route('/api/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    data = request.form
    image = request.files.get('image')
    
    db = get_db()
    product = Product.get_by_id(db, product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    image_url = product['image_url']
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'products', filename)
        image.save(image_path)
        image_url = f'/uploads/products/{filename}'
    
    Product.update(
        db,
        product_id,
        name=data.get('name', product['name']),
        category=data.get('category', product['category']),
        description=data.get('description', product['description']),
        image_url=image_url
    )
    
    updated_product = Product.get_by_id(db, product_id)
    return jsonify(updated_product), 200

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    db = get_db()
    Product.delete(db, product_id)
    return jsonify({'message': 'Product deleted successfully'}), 200

# ==================== BLOG ROUTES ====================

@app.route('/api/blog', methods=['GET'])
def get_blog_posts():
    db = get_db()
    posts = BlogPost.get_all(db)
    return jsonify(posts), 200

@app.route('/api/blog/<int:post_id>', methods=['GET'])
def get_blog_post(post_id):
    db = get_db()
    post = BlogPost.get_by_id(db, post_id)
    
    if post:
        return jsonify(post), 200
    
    return jsonify({'error': 'Blog post not found'}), 404

@app.route('/api/blog', methods=['POST'])
@jwt_required()
def create_blog_post():
    data = request.form
    image = request.files.get('image')
    
    image_url = None
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'blog', filename)
        image.save(image_path)
        image_url = f'/uploads/blog/{filename}'
    
    db = get_db()
    post_id = BlogPost.create(
        db,
        title=data.get('title'),
        content=data.get('content'),
        author=data.get('author', 'Admin'),
        image_url=image_url
    )
    
    post = BlogPost.get_by_id(db, post_id)
    return jsonify(post), 201

@app.route('/api/blog/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_blog_post(post_id):
    data = request.form
    image = request.files.get('image')
    
    db = get_db()
    post = BlogPost.get_by_id(db, post_id)
    
    if not post:
        return jsonify({'error': 'Blog post not found'}), 404
    
    image_url = post['image_url']
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'blog', filename)
        image.save(image_path)
        image_url = f'/uploads/blog/{filename}'
    
    BlogPost.update(
        db,
        post_id,
        title=data.get('title', post['title']),
        content=data.get('content', post['content']),
        author=data.get('author', post['author']),
        image_url=image_url
    )
    
    updated_post = BlogPost.get_by_id(db, post_id)
    return jsonify(updated_post), 200

@app.route('/api/blog/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_blog_post(post_id):
    db = get_db()
    BlogPost.delete(db, post_id)
    return jsonify({'message': 'Blog post deleted successfully'}), 200

# ==================== GALLERY ROUTES ====================

@app.route('/api/gallery', methods=['GET'])
def get_gallery_items():
    db = get_db()
    items = GalleryItem.get_all(db)
    return jsonify(items), 200

@app.route('/api/gallery', methods=['POST'])
@jwt_required()
def create_gallery_item():
    data = request.form
    file = request.files.get('file')
    
    if not file or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file'}), 400
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'gallery', filename)
    file.save(file_path)
    
    file_ext = filename.rsplit('.', 1)[1].lower()
    media_type = 'video' if file_ext in ['mp4', 'webm', 'ogg'] else 'image'
    
    db = get_db()
    item_id = GalleryItem.create(
        db,
        media_type=media_type,
        media_url=f'/uploads/gallery/{filename}',
        title=data.get('title', ''),
        description=data.get('description', '')
    )
    
    item = GalleryItem.get_by_id(db, item_id)
    return jsonify(item), 201

@app.route('/api/gallery/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_gallery_item(item_id):
    db = get_db()
    GalleryItem.delete(db, item_id)
    return jsonify({'message': 'Gallery item deleted successfully'}), 200

# ==================== CHATBOT ROUTES ====================

@app.route('/api/chatbot/settings', methods=['GET'])
def get_chatbot_settings():
    db = get_db()
    settings = ChatbotSettings.get(db)
    return jsonify(settings), 200

@app.route('/api/chatbot/settings', methods=['PUT'])
@jwt_required()
def update_chatbot_settings():
    data = request.get_json()
    db = get_db()
    
    ChatbotSettings.update(
        db,
        greeting=data.get('greeting'),
        faqs=json.dumps(data.get('faqs', []))
    )
    
    settings = ChatbotSettings.get(db)
    return jsonify(settings), 200

@app.route('/api/chatbot/message', methods=['POST'])
def chatbot_message():
    data = request.get_json()
    message = data.get('message', '').lower()
    
    db = get_db()
    settings = ChatbotSettings.get(db)
    faqs = json.loads(settings.get('faqs', '[]'))
    
    # Simple FAQ matching
    for faq in faqs:
        if any(keyword in message for keyword in faq.get('keywords', [])):
            return jsonify({'response': faq.get('answer', '')}), 200
    
    return jsonify({
        'response': 'Thank you for your message. For specific inquiries, please contact us through our contact form or email us at info@sinfinimarketing.com'
    }), 200

# ==================== DASHBOARD STATS ====================

@app.route('/api/dashboard/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    db = get_db()
    
    products_count = len(Product.get_all(db))
    blog_posts_count = len(BlogPost.get_all(db))
    gallery_items_count = len(GalleryItem.get_all(db))
    
    return jsonify({
        'products': products_count,
        'blog_posts': blog_posts_count,
        'gallery_items': gallery_items_count
    }), 200

# ==================== FILE SERVING ====================

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ==================== HELPER FUNCTIONS ====================

def send_email(to_email, subject, body, html_body=None):
    """Send email using SMTP"""
    try:
        if not all([SMTP_USERNAME, SMTP_PASSWORD, SMTP_FROM_EMAIL]):
            print("SMTP configuration missing")
            return False
            
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{SMTP_FROM_NAME} <{SMTP_FROM_EMAIL}>"
        msg['To'] = to_email
        
        # Add plain text part
        text_part = MIMEText(body, 'plain')
        msg.attach(text_part)
        
        # Add HTML part if provided
        if html_body:
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
        
        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def save_to_google_sheets(data):
    """Save contact form data to Google Sheets"""
    try:
        if not all([GOOGLE_SHEETS_CREDENTIALS_FILE, GOOGLE_SHEETS_SPREADSHEET_ID]):
            print("Google Sheets configuration missing")
            return False
            
        # Check if credentials file exists
        if not os.path.exists(GOOGLE_SHEETS_CREDENTIALS_FILE):
            print(f"Credentials file not found: {GOOGLE_SHEETS_CREDENTIALS_FILE}")
            return False
            
        # Set up credentials with new google-auth
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds = Credentials.from_service_account_file(GOOGLE_SHEETS_CREDENTIALS_FILE, scopes=scope)
        client = gspread.authorize(creds)
        
        # Open spreadsheet and worksheet
        sheet = client.open_by_key(GOOGLE_SHEETS_SPREADSHEET_ID)
        
        # Try to get existing worksheet or create new one
        try:
            worksheet = sheet.worksheet(GOOGLE_SHEETS_WORKSHEET_NAME)
        except gspread.WorksheetNotFound:
            print(f"Worksheet '{GOOGLE_SHEETS_WORKSHEET_NAME}' not found, creating it...")
            worksheet = sheet.add_worksheet(title=GOOGLE_SHEETS_WORKSHEET_NAME, rows="1000", cols="20")
        
        # Prepare row data
        from datetime import datetime
        row_data = [
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            data.get('name', ''),
            data.get('email', ''),
            data.get('phone', ''),
            data.get('company', ''),
            data.get('subject', ''),
            data.get('message', '')
        ]
        
        # Add header row if sheet is empty
        try:
            existing_data = worksheet.get_all_records()
            if len(existing_data) == 0:
                header = ['Timestamp', 'Name', 'Email', 'Phone', 'Company', 'Subject', 'Message']
                worksheet.append_row(header)
        except Exception as header_error:
            print(f"Error checking/adding headers: {header_error}")
            # If we can't check existing data, just try to add headers
            header = ['Timestamp', 'Name', 'Email', 'Phone', 'Company', 'Subject', 'Message']
            worksheet.append_row(header)
        
        # Add data row
        worksheet.append_row(row_data)
        print("Successfully saved to Google Sheets")
        return True
        
    except Exception as e:
        print(f"Error saving to Google Sheets: {e}")
        import traceback
        traceback.print_exc()
        return False

# ==================== CONTACT FORM ====================

@app.route('/api/contact', methods=['POST'])
def contact_form():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field.capitalize()} is required'}), 400
        
        # Prepare email content
        subject = f"New Contact Form Submission: {data.get('subject', 'General Inquiry')}"
        
        # Plain text email body
        body = f"""
New contact form submission from Sinfini Marketing website:

Name: {data.get('name')}
Email: {data.get('email')}
Phone: {data.get('phone', 'Not provided')}
Company: {data.get('company', 'Not provided')}
Subject: {data.get('subject', 'General Inquiry')}

Message:
{data.get('message')}

---
This message was sent from the Sinfini Marketing contact form.
        """
        
        # HTML email body
        html_body = f"""
        <html>
        <body>
            <h2>New Contact Form Submission</h2>
            <p>A new message has been received from the Sinfini Marketing website:</p>
            
            <table style="border-collapse: collapse; width: 100%;">
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px; font-weight: bold;">Name:</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{data.get('name')}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px; font-weight: bold;">Email:</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{data.get('email')}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px; font-weight: bold;">Phone:</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{data.get('phone', 'Not provided')}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px; font-weight: bold;">Company:</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{data.get('company', 'Not provided')}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px; font-weight: bold;">Subject:</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{data.get('subject', 'General Inquiry')}</td>
                </tr>
            </table>
            
            <h3>Message:</h3>
            <p style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid #007bff;">
                {data.get('message').replace('\n', '<br>')}
            </p>
            
            <hr>
            <p style="color: #666; font-size: 12px;">
                This message was sent from the Sinfini Marketing contact form.
            </p>
        </body>
        </html>
        """
        
        # Send email
        email_sent = False
        if SMTP_FROM_EMAIL:
            email_sent = send_email(SMTP_FROM_EMAIL, subject, body, html_body)
        
        # Save to Google Sheets
        sheets_saved = save_to_google_sheets(data)
        
        # Return response
        if email_sent or sheets_saved:
            return jsonify({
                'message': 'Message sent successfully',
                'email_sent': email_sent,
                'sheets_saved': sheets_saved
            }), 200
        else:
            return jsonify({
                'error': 'Failed to process your message. Please try again later.',
                'email_sent': email_sent,
                'sheets_saved': sheets_saved
            }), 500
            
    except Exception as e:
        print(f"Error in contact form: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', '0') == '1'
    port = int(os.environ.get('PORT', '5000'))
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
