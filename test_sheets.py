#!/usr/bin/env python3
"""
Test script to verify Google Sheets integration
"""

import os
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

# Load environment variables
load_dotenv()

def test_google_sheets():
    """Test Google Sheets connection and basic operations"""
    
    # Get configuration
    GOOGLE_SHEETS_CREDENTIALS_FILE = os.getenv('GOOGLE_SHEETS_CREDENTIALS_FILE')
    GOOGLE_SHEETS_SPREADSHEET_ID = os.getenv('GOOGLE_SHEETS_SPREADSHEET_ID')
    GOOGLE_SHEETS_WORKSHEET_NAME = os.getenv('GOOGLE_SHEETS_WORKSHEET_NAME', 'Contact_Form_Submissions')
    
    print("Testing Google Sheets Integration...")
    print(f"Credentials file: {GOOGLE_SHEETS_CREDENTIALS_FILE}")
    print(f"Spreadsheet ID: {GOOGLE_SHEETS_SPREADSHEET_ID}")
    print(f"Worksheet name: {GOOGLE_SHEETS_WORKSHEET_NAME}")
    
    try:
        # Check if credentials file exists
        if not os.path.exists(GOOGLE_SHEETS_CREDENTIALS_FILE):
            print(f"❌ ERROR: Credentials file not found: {GOOGLE_SHEETS_CREDENTIALS_FILE}")
            return False
        
        print("✅ Credentials file found")
        
        # Set up credentials
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds = Credentials.from_service_account_file(GOOGLE_SHEETS_CREDENTIALS_FILE, scopes=scope)
        client = gspread.authorize(creds)
        
        print("✅ Google Sheets client authorized")
        
        # Open spreadsheet
        sheet = client.open_by_key(GOOGLE_SHEETS_SPREADSHEET_ID)
        print(f"✅ Spreadsheet opened: {sheet.title}")
        
        # Try to get existing worksheet or create new one
        try:
            worksheet = sheet.worksheet(GOOGLE_SHEETS_WORKSHEET_NAME)
            print(f"✅ Worksheet found: {GOOGLE_SHEETS_WORKSHEET_NAME}")
        except gspread.WorksheetNotFound:
            print(f"⚠️  Worksheet '{GOOGLE_SHEETS_WORKSHEET_NAME}' not found, creating it...")
            worksheet = sheet.add_worksheet(title=GOOGLE_SHEETS_WORKSHEET_NAME, rows="1000", cols="20")
            print(f"✅ Worksheet created: {GOOGLE_SHEETS_WORKSHEET_NAME}")
        
        # Test writing data
        from datetime import datetime
        test_data = [
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Test User',
            'test@example.com',
            '+1234567890',
            'Test Company',
            'Test Subject',
            'This is a test message from the test script.'
        ]
        
        # Add header if needed
        try:
            existing_data = worksheet.get_all_records()
            if len(existing_data) == 0:
                header = ['Timestamp', 'Name', 'Email', 'Phone', 'Company', 'Subject', 'Message']
                worksheet.append_row(header)
                print("✅ Header row added")
        except Exception as e:
            print(f"⚠️  Could not check existing data, adding header anyway: {e}")
            header = ['Timestamp', 'Name', 'Email', 'Phone', 'Company', 'Subject', 'Message']
            worksheet.append_row(header)
        
        # Add test data
        worksheet.append_row(test_data)
        print("✅ Test data added successfully")
        
        print("\n🎉 Google Sheets integration test PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_google_sheets()
    if success:
        print("\n✅ All tests passed! Your Google Sheets integration is working correctly.")
    else:
        print("\n❌ Tests failed. Please check your configuration and try again.")
