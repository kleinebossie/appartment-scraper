#!/usr/bin/env python3
"""
SendGrid Email Notifier
Streamlined email notification system using only SendGrid.
"""

import requests
import json
import os
import logging
from typing import List, Dict
from datetime import datetime
from config import SENDGRID_API_KEY, SENDGRID_FROM_EMAIL, RECIPIENT_EMAIL

logger = logging.getLogger(__name__)


class SendGridNotifier:
    def __init__(self):
        self.api_key = SENDGRID_API_KEY
        self.from_email = SENDGRID_FROM_EMAIL
        self.to_email = RECIPIENT_EMAIL
        self.notification_file = "notifications.json"
    
    def create_email_content(self, listings: List[Dict]) -> str:
        """Create HTML email content for the listings."""
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .listing {{ border: 1px solid #ddd; margin: 15px 0; padding: 20px; border-radius: 8px; background-color: #fafafa; }}
                .title {{ color: #2c3e50; font-size: 18px; font-weight: bold; margin-bottom: 10px; }}
                .price {{ color: #e74c3c; font-size: 16px; font-weight: bold; margin: 5px 0; }}
                .location {{ color: #7f8c8d; margin: 5px 0; }}
                .details {{ color: #34495e; margin: 5px 0; }}
                .link {{ color: #3498db; text-decoration: none; font-weight: bold; }}
                .header {{ background-color: #ecf0f1; padding: 20px; border-radius: 8px; margin-bottom: 20px; text-align: center; }}
                .footer {{ text-align: center; margin-top: 20px; color: #7f8c8d; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🏠 New Apartment Listings Found!</h1>
                    <p>New apartment listings have been found on Pararius for Delft (€0-1500, 2 bedrooms, 10km radius).</p>
                    <p><strong>Found: {len(listings)} new listing(s)</strong></p>
                </div>
        """
        
        for listing in listings:
            html_content += f"""
                <div class="listing">
                    <div class="title">{listing['title']}</div>
                    <div class="price">{listing['price']}</div>
                    <div class="location">📍 {listing['location']}</div>
                    <div class="details">📋 {listing['details']}</div>
                    <div style="margin-top: 10px;">
                        <a href="{listing['link']}" class="link" target="_blank">View Listing →</a>
                    </div>
                </div>
            """
        
        html_content += f"""
                <div class="footer">
                    <p>This notification was sent by your Apartment Scraper Agent</p>
                    <p>Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def send_email(self, listings: List[Dict]) -> bool:
        """Send email notification using SendGrid."""
        if not all([self.api_key, self.from_email, self.to_email]):
            logger.error("SendGrid configuration incomplete. Please check your .env file.")
            return False
        
        try:
            url = "https://api.sendgrid.com/v3/mail/send"
            
            # Create email content
            html_content = self.create_email_content(listings)
            
            payload = {
                "personalizations": [
                    {
                        "to": [{"email": self.to_email}]
                    }
                ],
                "from": {"email": self.from_email},
                "subject": f"🏠 {len(listings)} New Apartment Listing(s) Found in Delft!",
                "content": [
                    {
                        "type": "text/html",
                        "value": html_content
                    }
                ]
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            logger.info(f"Email notification sent successfully to {self.to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email notification: {e}")
            return False
    
    def save_local_notification(self, listings: List[Dict]) -> bool:
        """Save notifications to a local file for backup."""
        try:
            notification_data = {
                "timestamp": datetime.now().isoformat(),
                "count": len(listings),
                "listings": listings
            }
            
            # Load existing notifications
            existing_notifications = []
            if os.path.exists(self.notification_file):
                try:
                    with open(self.notification_file, 'r', encoding='utf-8') as f:
                        existing_notifications = json.load(f)
                    logger.info(f"Loaded {len(existing_notifications)} existing notifications from {self.notification_file}")
                except Exception as e:
                    logger.warning(f"Error loading existing notifications from {self.notification_file}: {e}")
                    existing_notifications = []
            else:
                logger.info(f"No existing notifications file found at {self.notification_file}, creating new one")
            
            # Add new notification
            existing_notifications.append(notification_data)
            
            # Keep only last 50 notifications
            if len(existing_notifications) > 50:
                existing_notifications = existing_notifications[-50:]
                logger.info(f"Trimmed notifications to last 50 entries")
            
            # Save to file
            with open(self.notification_file, 'w', encoding='utf-8') as f:
                json.dump(existing_notifications, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Successfully saved {len(listings)} new listings to {self.notification_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving local notification to {self.notification_file}: {e}")
            # Try to create the directory if it doesn't exist
            try:
                os.makedirs(os.path.dirname(self.notification_file) if os.path.dirname(self.notification_file) else '.', exist_ok=True)
                with open(self.notification_file, 'w', encoding='utf-8') as f:
                    json.dump([notification_data], f, indent=2, ensure_ascii=False)
                logger.info(f"Successfully created and saved {len(listings)} new listings to {self.notification_file}")
                return True
            except Exception as e2:
                logger.error(f"Failed to create and save notification: {e2}")
                return False
    
    def print_notification(self, listings: List[Dict]) -> bool:
        """Print notifications to console."""
        try:
            print("\n" + "="*60)
            print(f"🏠 NEW APARTMENT LISTINGS FOUND! ({len(listings)} listings)")
            print("="*60)
            
            for i, listing in enumerate(listings, 1):
                print(f"\n{i}. {listing['title']}")
                print(f"   💰 {listing['price']}")
                print(f"   📍 {listing['location']}")
                print(f"   📋 {listing['details']}")
                print(f"   🔗 {listing['link']}")
            
            print("\n" + "="*60)
            return True
            
        except Exception as e:
            logger.error(f"Error printing notification: {e}")
            return False
    
    def send_notification(self, listings: List[Dict]) -> bool:
        """Send notifications using SendGrid and local backup."""
        if not listings:
            return True
        
        success = False
        
        # Method 1: Send email via SendGrid
        if self.send_email(listings):
            success = True
        
        # Method 2: Save to local file (backup)
        if self.save_local_notification(listings):
            success = True
        
        # Method 3: Print to console (immediate feedback)
        if self.print_notification(listings):
            success = True
        
        return success
    
    def test_notification_system(self) -> bool:
        """Test the notification system."""
        test_listing = {
            'title': 'Test Apartment Listing',
            'price': '€1,200',
            'location': 'Test Location, Delft',
            'details': 'Test details - 2 bedrooms, 60m²',
            'link': 'https://www.pararius.nl'
        }
        
        logger.info("Testing notification system...")
        
        # Test SendGrid email
        logger.info("Testing SendGrid email...")
        email_success = self.send_email([test_listing])
        if email_success:
            logger.info("✅ SendGrid email test successful!")
        else:
            logger.warning("✗ SendGrid email test failed")
        
        # Test local file
        logger.info("Testing local file notification...")
        local_success = self.save_local_notification([test_listing])
        if local_success:
            logger.info("✅ Local file notification test successful!")
        else:
            logger.error("✗ Local file notification test failed")
        
        # Test console output
        logger.info("Testing console notification...")
        console_success = self.print_notification([test_listing])
        if console_success:
            logger.info("✅ Console notification test successful!")
        else:
            logger.error("✗ Console notification test failed")
        
        return email_success or local_success or console_success 