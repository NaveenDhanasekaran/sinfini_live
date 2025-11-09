# 🚀 Quick Start Guide

Get your Sinfini Marketing website up and running in minutes!

## Step 1: Backend Setup

Open a terminal and run:

```bash
# Navigate to backend
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Initialize the database (creates admin user)
python database.py

# Add sample products, blog posts, and gallery items with images
python seed_data.py

# Start the Flask server
python app.py
```

✅ Backend should now be running on **http://localhost:5000**

## Step 2: Frontend Setup

Open a **NEW** terminal window and run:

```bash
# Navigate to frontend
cd frontend

# Install Node dependencies
npm install

# Start the React development server
npm start
```

✅ Frontend should now be running on **http://localhost:3000**

The website will automatically open in your browser!

## Step 3: Access Admin Panel

1. Go to **http://localhost:3000/admin/login**
2. Login with default credentials:
   - **Username**: `admin`
   - **Password**: `admin123`

## 🎯 What's Next?

### Add Your First Product
1. Go to Admin → Products
2. Click "Add Product"
3. Fill in details and upload an image
4. Click "Create"

### Write Your First Blog Post
1. Go to Admin → Blog Posts
2. Click "Add Post"
3. Use the rich text editor to create content
4. Upload a featured image
5. Click "Create"

### Upload Gallery Media
1. Go to Admin → Gallery
2. Click "Add Media"
3. Upload images or videos
4. Add titles and descriptions
5. Click "Upload"

### Configure Chatbot
1. Go to Admin → Chatbot
2. Edit the greeting message
3. Add FAQs with keywords
4. Click "Save Changes"

## 📱 Test the Public Website

Visit these pages:
- **Home**: http://localhost:3000/
- **About**: http://localhost:3000/about
- **Products**: http://localhost:3000/products
- **Gallery**: http://localhost:3000/gallery
- **Blog**: http://localhost:3000/blog
- **Contact**: http://localhost:3000/contact

## 🤖 Test the Chatbot

Look for the chat icon in the bottom-right corner on any public page!

## 🎨 Customize Colors

Edit `frontend/tailwind.config.js` to change the navy and gold colors.

## 🔒 Security Tips

1. **Change admin password** immediately in production
2. **Update secret keys** in `backend/app.py`
3. **Enable HTTPS** for production deployment

## ⚠️ Troubleshooting

### Port Already in Use
- Backend: Change port in `app.py`: `app.run(debug=True, port=5001)`
- Frontend: Set env variable: `PORT=3001 npm start`

### Database Issues
Delete `backend/sinfin_database.db` and run `python database.py` again

### Module Not Found
Make sure you're in the correct directory and ran `pip install` or `npm install`

## 📞 Need Help?

Check the main README.md for detailed documentation!

---

Happy Building! 🎉
