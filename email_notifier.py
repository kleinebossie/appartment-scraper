import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
import logging
from config import SMTP_SERVER, SMTP_PORT, EMAIL_USER, EMAIL_PASSWORD, RECIPIENT_EMAIL

logger = logging.getLogger(__name__)


class EmailNotifier:
    def __init__(self):
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.email_user = EMAIL_USER
        self.email_password = EMAIL_PASSWORD
        self.recipient_email = RECIPIENT_EMAIL
    
    def create_email_content(self, listings: List[Dict]) -> str:
        """Create HTML email content for the listings."""
        html_content = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .listing { border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }
                .title { color: #2c3e50; font-size: 18px; font-weight: bold; margin-bottom: 10px; }
                .price { color: #e74c3c; font-size: 16px; font-weight: bold; }
                .location { color: #7f8c8d; margin: 5px 0; }
                .details { color: #34495e; margin: 5px 0; }
                .link { color: #3498db; text-decoration: none; }
                .link:hover { text-decoration: underline; }
                .header { background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🏠 New Apartment Listings Found!</h1>
                <p>New apartment listings have been found on Pararius for Delft (€0-1500, 2 bedrooms, 10km radius).</p>
            </div>
        """
        
        for listing in listings:
            html_content += f"""
            <div class="listing">
                <div class="title">{listing['title']}</div>
                <div class="price">{listing['price']}</div>
                <div class="location">📍 {listing['location']}</div>
                <div class="details">📋 {listing['details']}</div>
                <div><a href="{listing['link']}" class="link" target="_blank">View Listing →</a></div>
            </div>
            """
        
        html_content += """
        </body>
        </html>
        """
        
        return html_content
    
    def send_notification(self, listings: List[Dict]) -> bool:
        """Send email notification with new listings."""
        if not all([self.email_user, self.email_password, self.recipient_email]):
            logger.error("Email configuration incomplete. Please check your .env file.")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🏠 {len(listings)} New Apartment Listing(s) Found in Delft!"
            msg['From'] = self.email_user
            msg['To'] = self.recipient_email
            
            # Create HTML content
            html_content = self.create_email_content(listings)
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.send_message(msg)
            
            logger.info(f"Email notification sent successfully to {self.recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email notification: {e}")
            return False
    
    def test_email_configuration(self) -> bool:
        """Test email configuration by sending a test email."""
        test_listing = {
            'title': 'Test Apartment Listing',
            'price': '€1,200',
            'location': 'Test Location, Delft',
            'details': 'Test details',
            'link': 'https://www.pararius.nl'
        }
        
        logger.info("Sending test email...")
        success = self.send_notification([test_listing])
        
        if success:
            logger.info("Test email sent successfully!")
        else:
            logger.error("Failed to send test email. Please check your email configuration.")
        
        return success 