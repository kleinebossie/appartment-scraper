# Apartment Scraper Agent

A Python agent that automatically scrapes apartment listings from Pararius.nl for Delft and sends email notifications when new listings appear.

## Features

- 🏠 Scrapes apartment listings from Pararius.nl for Delft (€0-1500, 2 bedrooms, 10km radius)
- 📧 Sends beautiful HTML email notifications for new listings
- ⏰ Configurable check intervals (default: 30 minutes)
- 💾 Tracks previously seen listings to avoid duplicate notifications
- 🔄 Continuous monitoring with graceful shutdown
- 📝 Comprehensive logging
- 🧪 Built-in testing capabilities

## Requirements

- Python 3.7+
- Internet connection
- Email account (Gmail recommended)

## Installation

1. **Clone or download the project files**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up email configuration:**
   
   Create a `.env` file in the project directory:
   ```bash
   cp env_example.txt .env
   ```
   
   Edit the `.env` file with your email credentials:
   ```
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   EMAIL_USER=your-email@gmail.com
   EMAIL_PASSWORD=your-app-password
   RECIPIENT_EMAIL=your-email@gmail.com
   ```

   **For Gmail users:** If you have 2-factor authentication enabled, you'll need to create an "App Password":
   1. Go to your Google Account settings
   2. Navigate to Security → 2-Step Verification → App passwords
   3. Generate a new app password for "Mail"
   4. Use this password in your `.env` file

## Usage

### Test the Setup

Before running the agent, test all components:

```bash
python main.py --test
```

This will:
- Test the scraper by fetching current listings
- Send a test email to verify your email configuration

### Run Once

To run the scraper once and exit:

```bash
python main.py --once
```

### Run Continuously

To start the agent for continuous monitoring:

```bash
python main.py
```

The agent will:
- Check for new listings every 30 minutes (configurable)
- Send email notifications when new listings are found
- Log all activities to both console and `apartment_scraper.log`

### Custom Check Interval

To override the default 30-minute interval:

```bash
python main.py --interval 15  # Check every 15 minutes
```

## Configuration

### Email Settings

Edit the `.env` file to configure your email settings:

- `SMTP_SERVER`: Your email provider's SMTP server (default: smtp.gmail.com)
- `SMTP_PORT`: SMTP port (default: 587)
- `EMAIL_USER`: Your email address
- `EMAIL_PASSWORD`: Your email password or app password
- `RECIPIENT_EMAIL`: Where to send notifications

### Scraping Settings

Edit `config.py` to modify scraping behavior:

- `TARGET_URL`: The Pararius search URL to monitor
- `CHECK_INTERVAL_MINUTES`: How often to check for new listings
- `HEADERS`: Browser headers to avoid being blocked

## How It Works

1. **Scraping**: The agent fetches the Pararius search page and extracts listing information including title, price, location, and details.

2. **Tracking**: Previously seen listings are stored in `seen_listings.json` to avoid duplicate notifications.

3. **Detection**: New listings are identified by comparing current listings with previously seen ones.

4. **Notification**: When new listings are found, a beautifully formatted HTML email is sent with all the details and direct links to the listings.

5. **Logging**: All activities are logged to both console and file for monitoring and debugging.

## File Structure

```
apartment-scraper/
├── main.py              # Main application entry point
├── scraper.py           # Web scraping logic
├── email_notifier.py    # Email notification system
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── env_example.txt      # Example environment variables
├── README.md           # This file
├── apartment_scraper.log # Application logs
└── seen_listings.json   # Tracked listings (created automatically)
```

## Troubleshooting

### Common Issues

1. **"Email configuration incomplete"**
   - Make sure your `.env` file exists and contains all required email settings
   - For Gmail, ensure you're using an App Password if 2FA is enabled

2. **"Error fetching page"**
   - Check your internet connection
   - The website might be temporarily unavailable
   - The website structure might have changed (check the scraper code)

3. **"Failed to send test email"**
   - Verify your email credentials
   - Check if your email provider allows SMTP access
   - For Gmail, ensure "Less secure app access" is enabled or use App Passwords

4. **No listings found**
   - The website structure might have changed
   - Check if the target URL is still valid
   - Run with `--test` to debug the scraper

### Logs

Check the `apartment_scraper.log` file for detailed error messages and debugging information.

### Website Changes

If Pararius changes their website structure, you may need to update the CSS selectors in `scraper.py`. The current selectors are:

- Listing containers: `li.search-list__item`
- Title and link: `a.listing-search-item__link`
- Price: `div.listing-search-item__price`
- Location: `div.listing-search-item__location`
- Details: `div.listing-search-item__details`

## Legal Notice

This tool is for personal use only. Please respect the website's terms of service and robots.txt file. Consider implementing reasonable delays between requests to avoid overwhelming the server.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.

## License

This project is open source and available under the MIT License. 