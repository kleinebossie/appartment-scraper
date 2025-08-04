import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Website configuration
TARGET_URL = "https://www.pararius.nl/huurwoningen/delft/0-1500/straal-10/2-slaapkamers"
CHECK_INTERVAL_MINUTES = int(os.getenv('CHECK_INTERVAL_MINUTES', 30))  # How often to check for new listings

# SendGrid configuration
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
SENDGRID_FROM_EMAIL = os.getenv('SENDGRID_FROM_EMAIL')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')

# File to store previously seen listings
LISTINGS_FILE = 'seen_listings.json'

# Headers to mimic a real browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
} 