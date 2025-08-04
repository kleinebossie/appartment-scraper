#!/usr/bin/env python3
"""
Simple test script for the apartment scraper
"""

try:
    from scraper import ParariusScraper
    import json
    
    print("Testing apartment scraper...")
    
    # Create scraper instance
    scraper = ParariusScraper()
    
    # Get current listings
    print("Fetching listings from Pararius...")
    listings = scraper.get_current_listings()
    
    print(f"Found {len(listings)} listings")
    
    if listings:
        print("\nSample listings:")
        for i, listing in enumerate(listings[:3], 1):
            print(f"{i}. {listing['title']}")
            print(f"   Price: {listing['price']}")
            print(f"   Location: {listing['location']}")
            print(f"   Link: {listing['link']}")
            print()
        
        # Save sample to file for inspection
        with open('sample_listings.json', 'w') as f:
            json.dump(listings[:5], f, indent=2, ensure_ascii=False)
        print("Saved sample listings to 'sample_listings.json'")
    else:
        print("No listings found. This might indicate:")
        print("- Website structure has changed")
        print("- Network connectivity issues")
        print("- Website is temporarily unavailable")
        
except ImportError as e:
    print(f"Import error: {e}")
    print("Please install dependencies: pip install -r requirements.txt")
except Exception as e:
    print(f"Error: {e}")
    print("Check the error message above for troubleshooting") 