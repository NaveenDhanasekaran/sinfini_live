# Google Sheets Integration Setup Guide

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Sheets API and Google Drive API

## Step 2: Create Service Account

1. Go to "IAM & Admin" > "Service Accounts"
2. Click "Create Service Account"
3. Give it a name like "sinfini-contact-form"
4. Click "Create and Continue"
5. Skip role assignment for now
6. Click "Done"

## Step 3: Generate Service Account Key

1. Click on the created service account
2. Go to "Keys" tab
3. Click "Add Key" > "Create new key"
4. Choose "JSON" format
5. Download the JSON file
6. Save it securely in your project (e.g., `credentials/service-account-key.json`)

## Step 4: Create Google Spreadsheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new spreadsheet
3. Name it "Sinfini Contact Form Submissions"
4. Note the spreadsheet ID from the URL (the long string between `/d/` and `/edit`)
5. Share the spreadsheet with your service account email (found in the JSON file)
   - Give "Editor" permissions to the service account email

## Step 5: Configure Environment Variables

Create a `.env` file in the backend directory with:

```env
# SMTP Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password_here
SMTP_FROM_EMAIL=your_email@gmail.com
SMTP_FROM_NAME=Sinfini Marketing FZC

# Google Sheets Configuration
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials/service-account-key.json
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id_here
GOOGLE_SHEETS_WORKSHEET_NAME=Sheet1

# Application Configuration
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET_KEY=jwt-secret-key-change-in-production
```

## Step 6: Gmail App Password Setup

1. Enable 2-Factor Authentication on your Gmail account
2. Go to Google Account settings
3. Security > 2-Step Verification > App passwords
4. Generate an app password for "Mail"
5. Use this app password in the `SMTP_PASSWORD` field

## Step 7: Test the Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Start the application: `python app.py`
3. Submit a test message through the contact form
4. Check your email and Google Sheets for the submission

## Spreadsheet Structure

The contact form will automatically create headers and populate data in this format:

| Timestamp | Name | Email | Phone | Company | Subject | Message |
|-----------|------|-------|-------|---------|---------|---------|
| 2024-11-09 15:30:00 | John Doe | john@example.com | +1234567890 | ABC Corp | General Inquiry | Hello, I'm interested... |

## Security Notes

- Keep your service account JSON file secure and never commit it to version control
- Add `credentials/` to your `.gitignore` file
- Use environment variables for all sensitive configuration
- Regularly rotate your app passwords and service account keys
