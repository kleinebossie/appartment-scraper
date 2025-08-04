#!/usr/bin/env python3
"""
Railway Scheduled Job Script
Runs the apartment scraper once and exits - perfect for Railway's cron scheduling.
"""

import sys
import logging
from main import ApartmentScraperAgent

# Set up logging for Railway
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Run the scraper once and exit."""
    try:
        logger.info("Starting Railway scheduled apartment scraper job...")
        
        agent = ApartmentScraperAgent()
        agent.run_once()
        
        logger.info("Railway scheduled job completed successfully!")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"Railway scheduled job failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 