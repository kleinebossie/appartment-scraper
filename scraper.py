import requests
import json
import time
import os
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import logging
from config import TARGET_URL, HEADERS, LISTINGS_FILE

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ParariusScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
    
    def fetch_page(self, url: str) -> Optional[str]:
        """Fetch the webpage content."""
        try:
            logger.info(f"Fetching page: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching page: {e}")
            return None
    
    def parse_listings(self, html_content: str) -> List[Dict]:
        """Parse apartment listings from the HTML content."""
        listings = []
        soup = BeautifulSoup(html_content, 'lxml')
        
        # Find all listing containers
        listing_containers = soup.find_all('li', class_='search-list__item')
        
        for container in listing_containers:
            try:
                listing = self._extract_listing_data(container)
                if listing:
                    listings.append(listing)
            except Exception as e:
                logger.error(f"Error parsing listing: {e}")
                continue
        
        logger.info(f"Found {len(listings)} listings")
        return listings
    
    def _extract_listing_data(self, container) -> Optional[Dict]:
        """Extract data from a single listing container."""
        try:
            # Extract title and link
            title_elem = container.find('a', class_='listing-search-item__link')
            if not title_elem:
                return None
            
            title = title_elem.get_text(strip=True)
            link = title_elem.get('href')
            if link and not link.startswith('http'):
                link = f"https://www.pararius.nl{link}"
            
            # Extract price
            price_elem = container.find('div', class_='listing-search-item__price')
            price = price_elem.get_text(strip=True) if price_elem else "Price not available"
            
            # Extract location
            location_elem = container.find('div', class_='listing-search-item__location')
            location = location_elem.get_text(strip=True) if location_elem else "Location not available"
            
            # Extract details (bedrooms, size, etc.)
            details_elem = container.find('div', class_='listing-search-item__details')
            details = details_elem.get_text(strip=True) if details_elem else "Details not available"
            
            # Create unique identifier
            listing_id = f"{title}_{location}_{price}".replace(" ", "_").lower()
            
            return {
                'id': listing_id,
                'title': title,
                'price': price,
                'location': location,
                'details': details,
                'link': link,
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Error extracting listing data: {e}")
            return None
    
    def get_current_listings(self) -> List[Dict]:
        """Get current listings from the website."""
        html_content = self.fetch_page(TARGET_URL)
        if html_content:
            return self.parse_listings(html_content)
        return []
    
    def load_seen_listings(self) -> set:
        """Load previously seen listing IDs from file."""
        try:
            with open(LISTINGS_FILE, 'r') as f:
                data = json.load(f)
                seen_ids = set(data.get('seen_ids', []))
                logger.info(f"Successfully loaded {len(seen_ids)} seen listings from {LISTINGS_FILE}")
                return seen_ids
        except FileNotFoundError:
            logger.info(f"No previous listings file found at {LISTINGS_FILE}, starting fresh")
            return set()
        except Exception as e:
            logger.error(f"Error loading seen listings from {LISTINGS_FILE}: {e}")
            return set()
    
    def save_seen_listings(self, seen_ids: set):
        """Save seen listing IDs to file."""
        try:
            data = {'seen_ids': list(seen_ids)}
            with open(LISTINGS_FILE, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Successfully saved {len(seen_ids)} seen listings to {LISTINGS_FILE}")
        except Exception as e:
            logger.error(f"Error saving seen listings to {LISTINGS_FILE}: {e}")
            # Try to create the file if it doesn't exist
            try:
                os.makedirs(os.path.dirname(LISTINGS_FILE) if os.path.dirname(LISTINGS_FILE) else '.', exist_ok=True)
                with open(LISTINGS_FILE, 'w') as f:
                    json.dump(data, f, indent=2)
                logger.info(f"Successfully created and saved {len(seen_ids)} seen listings to {LISTINGS_FILE}")
            except Exception as e2:
                logger.error(f"Failed to create and save seen listings: {e2}")
    
    def get_new_listings(self) -> List[Dict]:
        """Get new listings that haven't been seen before."""
        current_listings = self.get_current_listings()
        seen_listings = self.load_seen_listings()
        
        logger.info(f"Loaded {len(seen_listings)} previously seen listings")
        logger.info(f"Found {len(current_listings)} current listings")
        
        new_listings = []
        current_ids = set()
        
        for listing in current_listings:
            current_ids.add(listing['id'])
            if listing['id'] not in seen_listings:
                new_listings.append(listing)
                logger.info(f"New listing found: {listing['id']}")
            else:
                logger.debug(f"Listing already seen: {listing['id']}")
        
        # Update seen listings with current ones
        self.save_seen_listings(current_ids)
        logger.info(f"Updated seen_listings.json with {len(current_ids)} listings")
        
        logger.info(f"Found {len(new_listings)} new listings")
        return new_listings 