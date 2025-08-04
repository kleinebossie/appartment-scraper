# Apartment Scraper Agent

A lightweight Python agent that automatically scrapes apartment listings from Pararius.nl for Delft and sends email notifications when new listings appear using SendGrid.

## Features

- 🏠 Scrapes apartment listings from Pararius.nl for Delft (€0-1500, 2 bedrooms, 10km radius)
- 📧 Sends beautiful HTML email notifications via SendGrid
- ⏰ Configurable check intervals (default: 30 minutes)
- 💾 Tracks previously seen listings to avoid duplicate notifications
- 🔄 Continuous monitoring with graceful shutdown
- 📝 Comprehensive logging
- 🧪 Built-in testing capabilities
- 🚀 Optimized for performance and memory efficiency

## Requirements

- Python 3.7+
- Internet connection
- SendGrid account (free tier: 100 emails/day)

## Installation

1. **Clone or download the project files**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up SendGrid:**
   
   Create a `.env` file in the project directory:
   ```bash
   cp env_example.txt .env
   ```
   
   Edit the `.env` file with your SendGrid credentials:
   ```
   SENDGRID_API_KEY=SG.your_api_key_here
   SENDGRID_FROM_EMAIL=your_verified_email@gmail.com
   RECIPIENT_EMAIL=your_email@gmail.com
   ```

   **To get SendGrid credentials:**
   1. Sign up at [SendGrid](https://sendgrid.com/) (free)
   2. Go to Settings → API Keys → Create API Key
   3. Go to Settings → Sender Authentication → Verify a Single Sender
   4. Use your verified email as `SENDGRID_FROM_EMAIL`

## Usage

### Test the Setup

Before running the agent, test all components:

```bash
python3 main.py --test
```

This will:
- Test the scraper by fetching current listings
- Send a test email via SendGrid
- Test local file and console notifications

### Run Once

To run the scraper once and exit:

```bash
python3 main.py --once
```

### Run Continuously

To start the agent for continuous monitoring:

```bash
python3 main.py
```

The agent will:
- Check for new listings every 30 minutes (configurable)
- Send email notifications when new listings are found
- Log all activities to both console and `apartment_scraper.log`

### Custom Check Interval

To override the default 30-minute interval:

```bash
python3 main.py --interval 15  # Check every 15 minutes
```

## Configuration

### SendGrid Settings

Edit the `.env` file to configure SendGrid:

- `SENDGRID_API_KEY`: Your SendGrid API key (starts with "SG.")
- `SENDGRID_FROM_EMAIL`: Your verified sender email address
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

4. **Notification**: When new listings are found:
   - SendGrid email notification with beautiful HTML formatting
   - Local file backup (`notifications.json`)
   - Console output for immediate feedback

5. **Logging**: All activities are logged to both console and file for monitoring and debugging.

## File Structure

```
apartment-scraper/
├── main.py              # Main application entry point
├── scraper.py           # Web scraping logic
├── sendgrid_notifier.py # SendGrid email notification system
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── env_example.txt      # Example environment variables
├── README.md           # This file
├── apartment_scraper.log # Application logs
├── seen_listings.json   # Tracked listings (created automatically)
└── notifications.json   # Notification history (created automatically)
```

## Troubleshooting

### Common Issues

1. **"SendGrid configuration incomplete"**
   - Make sure your `.env` file exists and contains all required SendGrid settings
   - Verify your sender email is verified in SendGrid

2. **"Error fetching page"**
   - Check your internet connection
   - The website might be temporarily unavailable
   - The website structure might have changed (check the scraper code)

3. **"Failed to send test email"**
   - Verify your SendGrid API key is correct
   - Make sure your sender email is verified in SendGrid
   - Check if you've exceeded the free tier limit (100 emails/day)

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

## Performance Benefits

This streamlined version offers:

- **Reduced memory usage** - Only essential components loaded
- **Faster startup** - No complex OAuth2 or multiple email method checks
- **Simpler maintenance** - Single email service to manage
- **Better reliability** - SendGrid's professional email delivery
- **Lower resource consumption** - Optimized for long-running operation

## Legal Notice

This tool is for personal use only. Please respect the website's terms of service and robots.txt file. Consider implementing reasonable delays between requests to avoid overwhelming the server.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.

## License

This project is open source and available under the MIT License. 