#!/usr/bin/env python3
"""
Setup script for the apartment scraper
"""

import subprocess
import sys
import os

def run_command(command):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {command}")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🏠 Apartment Scraper Setup")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        sys.exit(1)
    
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        print("\n📝 Creating .env file...")
        if os.path.exists('env_example.txt'):
            with open('env_example.txt', 'r') as src:
                with open('.env', 'w') as dst:
                    dst.write(src.read())
            print("✓ Created .env file from template")
            print("⚠️  Please edit .env file with your email credentials")
        else:
            print("⚠️  env_example.txt not found, please create .env file manually")
    
    # Test the scraper
    print("\n🧪 Testing scraper...")
    if run_command(f"{sys.executable} test_scraper.py"):
        print("✓ Scraper test completed")
    else:
        print("⚠️  Scraper test failed, but setup completed")
    
    print("\n🎉 Setup completed!")
    print("\nNext steps:")
    print("1. Edit .env file with your email credentials")
    print("2. Run: python main.py --test")
    print("3. Run: python main.py (for continuous monitoring)")
    print("\nFor help, see README.md")

if __name__ == "__main__":
    main() 