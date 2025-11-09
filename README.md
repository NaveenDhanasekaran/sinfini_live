# Sinfini Marketing FZC - Professional Website

A professional, full-stack website for Sinfini Marketing FZC, a textile export company based in Sharjah, UAE.

## 🚀 Features

### Frontend
- **React** with React Router for navigation
- **Tailwind CSS** for modern, responsive design
- **Premium UI/UX** with navy, gold, and white color scheme
- Smooth animations and transitions
- Fully responsive design

### Public Pages
- **Home**: Hero slider, company intro, product highlights, CTA sections
- **About Us**: Company profile, mission, vision, values
- **Products**: Grid layout with product details modal
- **Gallery**: Image and video showcase with lightbox
- **Blog**: List and detailed blog post views
- **Contact**: Contact form with Google Maps integration

### Admin Panel
- **Secure Authentication**: JWT-based login system
- **Dashboard**: Overview statistics
- **Products Management**: Full CRUD operations with image upload
- **Blog Management**: WYSIWYG editor (React Quill) for rich content
- **Gallery Management**: Upload images and videos
- **Chatbot Settings**: Configure greeting messages and FAQs

### Chatbot
- Floating chat widget on public pages
- FAQ-based responses with keyword matching
- Customizable greeting and responses via admin panel

### Backend
- **Flask** RESTful API
- **SQLite** database
- **JWT** authentication
- File upload handling
- CORS enabled for local development

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## 🔧 Installation & Setup

### Quick Start (Recommended)

1. **One-time setup**:
```bash
# Install backend dependencies
pip install -r backend/requirements.txt

# Install frontend dependencies
cd frontend && npm install && cd ..
```

2. **Start both servers with one command**:
```bash
python app.py
```

This will start:
- Backend API on `http://localhost:5000`
- Frontend on `http://localhost:3000`

Press `Ctrl+C` to stop both servers.

### Manual Setup (Alternative)

#### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment (recommended):
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize database:
```bash
python database.py
```

5. (Optional) Add sample data with images:
```bash
python seed_data.py
```

6. Run the Flask server:
```bash
python app.py
```

Backend will run on `http://localhost:5000`

#### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

Frontend will run on `http://localhost:3000`

## 🔐 Default Admin Credentials

- **Username**: admin
- **Password**: admin123

**Important**: Change these credentials in production!

## 📁 Project Structure

```
sinfin_website/
├── app.py                  # 🚀 Main launcher (starts both servers)
├── render.yaml             # 🌐 Render deployment config
├── README.md
├── backend/
│   ├── app.py              # Flask application
│   ├── database.py         # Database initialization
│   ├── models.py           # Database models
│   ├── requirements.txt    # Python dependencies
│   └── uploads/            # Uploaded media files
│       ├── products/
│       ├── blog/
│       └── gallery/
└── frontend/
    ├── public/
    ├── src/
    │   ├── components/     # Reusable components
    │   ├── pages/          # Page components
    │   │   ├── admin/      # Admin panel pages
    │   │   └── ...         # Public pages
    │   ├── context/        # React context (Auth)
    │   ├── utils/          # API utilities
    │   ├── App.js
    │   └── index.js
    ├── package.json
    └── tailwind.config.js
```

## 🎨 Color Scheme

- **Navy**: Primary color (#102a43 - #334e68)
- **Gold**: Accent color (#d4a53d - #e8bf60)
- **White**: Background and text

## 🛠️ Technologies Used

### Frontend
- React 18
- React Router DOM 6
- Tailwind CSS 3
- Axios
- React Quill (WYSIWYG editor)
- Lucide React (icons)
- Headless UI

### Backend
- Flask 3
- Flask-CORS
- Flask-JWT-Extended
- SQLite3
- Werkzeug

## 📱 Features by Section

### Public Website
- Sticky navigation bar
- Hero slider with auto-rotation
- Product catalog with modal details
- Blog with rich text content
- Gallery with image/video support
- Contact form with validation
- Responsive footer with social links
- Chatbot for customer support

### Admin Dashboard
- Statistics overview
- Quick action links
- Secure authentication
- File upload management
- Rich text editor
- Real-time preview
- Responsive admin layout

## 🔒 Security Features

- JWT token authentication
- Password hashing with Werkzeug
- Protected admin routes
- File type validation
- File size limits
- CORS configuration

## 🚀 Deployment

### Backend
- Update `SECRET_KEY` and `JWT_SECRET_KEY` in `app.py`
- Configure production database
- Set up file storage (local or cloud)
- Use WSGI server (Gunicorn, uWSGI)

### Frontend
- Build production bundle: `npm run build`
- Deploy to static hosting (Netlify, Vercel, etc.)
- Update API base URL in `src/utils/api.js`

## 📝 API Endpoints

### Authentication
- POST `/api/auth/login` - Admin login
- GET `/api/auth/verify` - Verify token

### Products
- GET `/api/products` - Get all products
- GET `/api/products/:id` - Get single product
- POST `/api/products` - Create product (auth required)
- PUT `/api/products/:id` - Update product (auth required)
- DELETE `/api/products/:id` - Delete product (auth required)

### Blog
- GET `/api/blog` - Get all posts
- GET `/api/blog/:id` - Get single post
- POST `/api/blog` - Create post (auth required)
- PUT `/api/blog/:id` - Update post (auth required)
- DELETE `/api/blog/:id` - Delete post (auth required)

### Gallery
- GET `/api/gallery` - Get all items
- POST `/api/gallery` - Upload item (auth required)
- DELETE `/api/gallery/:id` - Delete item (auth required)

### Chatbot
- GET `/api/chatbot/settings` - Get chatbot settings
- PUT `/api/chatbot/settings` - Update settings (auth required)
- POST `/api/chatbot/message` - Send message

### Other
- GET `/api/dashboard/stats` - Get dashboard statistics (auth required)
- POST `/api/contact` - Submit contact form

## 🤝 Support

For support, email info@sinfinimarketing.com

## 📄 License

This project is proprietary and confidential.

---

Built with ❤️ for Sinfini Marketing FZC
"# sinfini_clean" 
"# sinfini_live" 
