#!/usr/bin/env python3
"""
Apartment Scraper Agent
Scrapes Pararius for apartment listings in Delft and sends email notifications for new listings.
"""

import time
import schedule
import logging
import signal
import sys
from datetime import datetime
from scraper import ParariusScraper
from sendgrid_notifier import SendGridNotifier
from config import CHECK_INTERVAL_MINUTES

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('apartment_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ApartmentScraperAgent:
    def __init__(self):
        self.scraper = ParariusScraper()
        self.notifier = SendGridNotifier()
        self.running = True
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        logger.info("Received shutdown signal. Stopping the agent...")
        self.running = False
        sys.exit(0)
    
    def check_for_new_listings(self):
        """Check for new listings and send notifications."""
        try:
            logger.info("Checking for new apartment listings...")
            
            # Get new listings
            new_listings = self.scraper.get_new_listings()
            
            if new_listings:
                logger.info(f"Found {len(new_listings)} new listing(s)!")
                
                # Send notification
                if self.notifier.send_notification(new_listings):
                    logger.info("Notification sent successfully!")
                    logger.info("notifications.json has been updated with the new listings.")
                else:
                    logger.error("Failed to send notification!")
                
                # Log the new listings
                for listing in new_listings:
                    logger.info(f"New listing: {listing['title']} - {listing['price']} - {listing['location']}")
            else:
                logger.info("No new listings found.")
                logger.info("seen_listings.json has been updated with current listings to prevent future duplicates.")
                
        except Exception as e:
            logger.error(f"Error during listing check: {e}")
    
    def run_once(self):
        """Run the scraper once and exit."""
        logger.info("Running apartment scraper once...")
        self.check_for_new_listings()
        logger.info("Single run completed.")
        logger.info("Both seen_listings.json and notifications.json have been updated.")
    
    def run_continuous(self):
        """Run the scraper continuously with scheduled checks."""
        import config
        logger.info(f"Starting apartment scraper agent (checking every {config.CHECK_INTERVAL_MINUTES} minutes)...")
        
        # Schedule the job
        schedule.every(config.CHECK_INTERVAL_MINUTES).minutes.do(self.check_for_new_listings)
        
        # Run initial check
        self.check_for_new_listings()
        
        # Keep running until interrupted
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute for scheduled tasks
            except KeyboardInterrupt:
                logger.info("Interrupted by user. Stopping...")
                break
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                time.sleep(60)  # Wait before retrying
        
        logger.info("Apartment scraper agent stopped.")
    
    def test_components(self):
        """Test all components of the system."""
        logger.info("Testing apartment scraper components...")
        
        # Test scraper
        logger.info("Testing scraper...")
        try:
            listings = self.scraper.get_current_listings()
            logger.info(f"Scraper test successful! Found {len(listings)} current listings.")
            
            if listings:
                logger.info("Sample listing:")
                sample = listings[0]
                logger.info(f"  Title: {sample['title']}")
                logger.info(f"  Price: {sample['price']}")
                logger.info(f"  Location: {sample['location']}")
        except Exception as e:
            logger.error(f"Scraper test failed: {e}")
            return False
        
        # Test notification system
        logger.info("Testing notification system...")
        if not self.notifier.test_notification_system():
            logger.error("Notification test failed!")
            return False
        
        logger.info("All component tests passed!")
        return True


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Apartment Scraper Agent')
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    parser.add_argument('--test', action='store_true', help='Test all components')
    parser.add_argument('--interval', type=int, help='Check interval in minutes (overrides config)')
    
    args = parser.parse_args()
    
    # Override interval if specified
    if args.interval:
        import config
        config.CHECK_INTERVAL_MINUTES = args.interval
        logger.info(f"Using custom interval: {config.CHECK_INTERVAL_MINUTES} minutes")
    
    agent = ApartmentScraperAgent()
    
    if args.test:
        success = agent.test_components()
        sys.exit(0 if success else 1)
    elif args.once:
        agent.run_once()
    else:
        agent.run_continuous()


if __name__ == "__main__":
    main() 