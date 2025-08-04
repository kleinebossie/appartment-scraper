#!/usr/bin/env python3
"""
Test SendGrid Configuration
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_sendgrid():
    """Test SendGrid API key and configuration."""
    
    print("🧪 Testing SendGrid Configuration")
    print("=" * 40)
    
    # Get credentials from .env
    api_key = os.getenv('SENDGRID_API_KEY')
    from_email = os.getenv('SENDGRID_FROM_EMAIL')
    to_email = os.getenv('RECIPIENT_EMAIL')
    
    if not all([api_key, from_email, to_email]):
        print("❌ Missing SendGrid configuration in .env file")
        print("Please make sure you have:")
        print("SENDGRID_API_KEY=SG.your_api_key")
        print("SENDGRID_FROM_EMAIL=your_verified_email@gmail.com")
        print("RECIPIENT_EMAIL=your_email@gmail.com")
        return False
    
    print(f"📧 From: {from_email}")
    print(f"📧 To: {to_email}")
    print(f"🔑 API Key: {api_key[:10]}...")
    print()
    
    try:
        # Test API key by making a simple request
        url = "https://api.sendgrid.com/v3/user/profile"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        print("🔄 Testing API key...")
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print("✅ API key is valid!")
            
            # Try to send a test email
            print("🔄 Sending test email...")
            
            email_url = "https://api.sendgrid.com/v3/mail/send"
            payload = {
                "personalizations": [
                    {
                        "to": [{"email": to_email}]
                    }
                ],
                "from": {"email": from_email},
                "subject": "🧪 SendGrid Test - Apartment Scraper",
                "content": [
                    {
                        "type": "text/html",
                        "value": """
                        <html>
                        <body>
                            <h2>🎉 SendGrid Test Successful!</h2>
                            <p>Your apartment scraper email notifications are now working with SendGrid.</p>
                            <p><strong>Configuration:</strong></p>
                            <ul>
                                <li>✅ API Key: Valid</li>
                                <li>✅ Sender Email: Verified</li>
                                <li>✅ Recipient Email: Configured</li>
                                <li>✅ Service: SendGrid</li>
                            </ul>
                            <p>You'll now receive notifications when new apartment listings are found!</p>
                        </body>
                        </html>
                        """
                    }
                ]
            }
            
            email_response = requests.post(email_url, json=payload, headers=headers)
            
            if email_response.status_code == 202:
                print("✅ Test email sent successfully!")
                print("🎉 SendGrid setup is working perfectly!")
                return True
            else:
                print(f"❌ Email sending failed: {email_response.status_code}")
                print(f"Response: {email_response.text}")
                return False
                
        else:
            print(f"❌ API key test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def setup_sendgrid_env():
    """Help user set up .env file for SendGrid."""
    
    print("🔧 SendGrid .env Setup Helper")
    print("=" * 30)
    print()
    
    if not os.path.exists('.env'):
        print("Creating .env file...")
        with open('.env', 'w') as f:
            f.write("# SendGrid Configuration\n")
            f.write("SENDGRID_API_KEY=\n")
            f.write("SENDGRID_FROM_EMAIL=\n")
            f.write("RECIPIENT_EMAIL=\n")
    
    print("📝 Please edit your .env file with:")
    print("SENDGRID_API_KEY=SG.your_api_key_here")
    print("SENDGRID_FROM_EMAIL=kleinebossie@gmail.com")
    print("RECIPIENT_EMAIL=kleinebossie@gmail.com")
    print()
    print("💡 Remember:")
    print("- Get your API key from SendGrid Settings → API Keys")
    print("- Verify your sender email in SendGrid Settings → Sender Authentication")
    print("- The API key starts with 'SG.'")
    print()

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Test SendGrid configuration")
    print("2. Setup .env file")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        test_sendgrid()
    elif choice == "2":
        setup_sendgrid_env()
    else:
        print("Invalid choice") 