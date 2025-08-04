#!/usr/bin/env python3
"""
Test script to verify duplicate detection and file updates.
"""

import json
import os
import logging
from scraper import ParariusScraper
from sendgrid_notifier import SendGridNotifier

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_duplicate_detection():
    """Test that duplicate detection is working properly."""
    logger.info("Testing duplicate detection...")
    
    # Initialize components
    scraper = ParariusScraper()
    notifier = SendGridNotifier()
    
    # Check current state of files
    logger.info("Checking current state of files...")
    
    if os.path.exists('seen_listings.json'):
        with open('seen_listings.json', 'r') as f:
            seen_data = json.load(f)
            logger.info(f"seen_listings.json contains {len(seen_data.get('seen_ids', []))} seen listings")
    else:
        logger.info("seen_listings.json does not exist")
    
    if os.path.exists('notifications.json'):
        with open('notifications.json', 'r') as f:
            notifications = json.load(f)
            logger.info(f"notifications.json contains {len(notifications)} notification entries")
    else:
        logger.info("notifications.json does not exist")
    
    # Run the scraper once
    logger.info("Running scraper to get new listings...")
    new_listings = scraper.get_new_listings()
    
    logger.info(f"Found {len(new_listings)} new listings")
    
    if new_listings:
        # Send notification
        logger.info("Sending notification...")
        success = notifier.send_notification(new_listings)
        logger.info(f"Notification sent: {success}")
    
    # Check final state of files
    logger.info("Checking final state of files...")
    
    if os.path.exists('seen_listings.json'):
        with open('seen_listings.json', 'r') as f:
            seen_data = json.load(f)
            logger.info(f"seen_listings.json now contains {len(seen_data.get('seen_ids', []))} seen listings")
    else:
        logger.error("seen_listings.json still does not exist!")
    
    if os.path.exists('notifications.json'):
        with open('notifications.json', 'r') as f:
            notifications = json.load(f)
            logger.info(f"notifications.json now contains {len(notifications)} notification entries")
    else:
        logger.error("notifications.json still does not exist!")
    
    # Test duplicate detection
    logger.info("Testing duplicate detection by running scraper again...")
    new_listings_2 = scraper.get_new_listings()
    logger.info(f"Second run found {len(new_listings_2)} new listings (should be 0 if duplicate detection works)")
    
    if len(new_listings_2) == 0:
        logger.info("✅ Duplicate detection is working correctly!")
    else:
        logger.warning("⚠️ Duplicate detection may not be working correctly")

if __name__ == "__main__":
    test_duplicate_detection() 