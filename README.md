# 🗺️ Google Maps Scraper

A powerful, production-ready Python web scraper for extracting business/place information from Google Maps without requiring an API key. Built on Selenium for reliable handling of dynamic JavaScript content and designed for both CLI usage and programmatic integration.

---

## ✨ Highlights

- ✅ No API key required — scrapes the Google Maps web UI
- ✅ Handles dynamic content with Selenium (headless optional)
- ✅ Export to Excel (.xlsx) and JSON (.json)
- ✅ Filters, sorting, duplicate detection, and configurable rate-limiting
- ✅ Designed for automation and developer integration

---

**Last Updated:** December 31, 2025  
**Version:** 1.0.0  
**Python:** 3.8+

## Table of Contents

- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [CLI Examples](#cli-examples)
  - [Programmatic API](#programmatic-api)
- [Cases (Use Cases & Examples)](#cases)
- [Advanced Configuration](#advanced-configuration)
- [Performance & Optimization Tips](#performance--optimization-tips)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License & Contact](#license--contact)

---

## Project Structure

```
google_maps_scraper/
├── main.py                  # CLI entry point
├── config.py                # Default configuration and constants
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── outputs/                 # Saved Excel/JSON outputs (auto-created)
├── logs/                    # Logging output (auto-created)
└── scraper/
   ├── __init__.py
   ├── google_maps.py       # Core scraping logic (search + details extraction)
   └── utils.py             # Helper functions (parsing, saving, dedupe)
```

Use this layout to integrate or extend the scraper. Keep `outputs/` and `logs/` writable by your runtime environment.

---

## Quick Start

1. Create a Python 3.8+ virtual environment

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run a quick smoke test

```bash
python -c "from selenium import webdriver; print('Selenium available')"
```

---

## Installation

Recommended: create and activate a virtual environment and install the pinned dependencies in `requirements.txt`.

- Chrome / Chromium is required for the Selenium WebDriver (unless you adapt to another driver).
- Ensure the ChromeDriver binary matches your installed Chrome/Chromium version, or use a WebDriver manager package.

If you prefer to pin versions explicitly, edit `requirements.txt` or use `pip-tools`.

---

## Configuration

Edit `config.py` to change defaults such as `default_location`, `max_results`, `timeout`, and `delay_between_requests`.

Example default options (in `config.py`):

```python
class Config:
   def __init__(self):
      self.default_location = 'United States'
      self.max_results = 20
      self.delay_between_requests = 1  # seconds
      self.timeout = 30  # seconds
      self.output_format = 'xlsx'  # 'xlsx', 'json' or 'both'
      self.headless = True
```

---

## Usage

### CLI

Run the CLI entry point `main.py`. Basic CLI options:

```
usage: main.py [-h] --search SEARCH [--location LOCATION] [--output OUTPUT]
          [--max-results MAX_RESULTS] [--min-rating MIN_RATING]
          [--format {xlsx,json,both}] [--sort-by {rating,reviews,name}]
          [--verbose]
```

Example commands:

```bash
# Search restaurants in New York
python main.py --search "restaurants" --location "New York"

# Limit results and export to JSON
python main.py --search "hotels" --location "Paris" --max-results 25 --format json

# Verbose logging
python main.py --search "coffee shops" --verbose
```

### CLI Examples

- Search + Excel: `python main.py --search "restaurants" --location "Tokyo" --max-results 30`
- Search + JSON: `python main.py --search "gyms" --format json`
- Filter by rating: `python main.py --search "bars" --min-rating 4.0`
- Sort by reviews: `python main.py --search "museums" --sort-by reviews`

Outputs are written to the `outputs/` directory by default and named with a timestamp.

### Programmatic API

You can use the scraper from Python code. Minimal example:

```python
from config import Config
from scraper.google_maps import GoogleMapsScraper
from scraper import utils

config = Config()
config.max_results = 50
config.headless = True
scraper = GoogleMapsScraper(config)

results = scraper.search_places("restaurants", "New York")
results = utils.filter_places_by_rating(results, 4.0)
results = utils.merge_duplicate_places(results)
scraper.save_to_excel(results, "outputs/google_maps_restaurants_nyc.xlsx")
```

Refer to `scraper/google_maps.py` for available methods and input parameter details.

---

## Cases (Use Cases & Examples)

1. Data collection for a local business directory
  - Search a category across target cities and export to Excel for contact outreach.

2. Market research (ratings & review counts)
  - Collect top results for categories and analyze rating distributions.

3. Lead generation
  - Extract phone and website fields, filter by rating and duplicate-deduplicate results.

4. Periodic monitoring
  - Schedule runs with a CI job and compare exports over time to detect changes.

---

## Advanced Configuration

- `headless`: run Chrome headless or visible for debugging
- `delay_between_requests`: randomize or add jitter to mimic slower browsing
- `user_agent`: rotate or set a realistic User-Agent string in `config.py` or the WebDriver options
- `proxy`: add proxy support in `google_maps.py` to distribute requests (note: proxies may have their own limitations)

Example of enabling headless in WebDriver options (pseudo-code):

```python
from selenium.webdriver.chrome.options import Options
opts = Options()
if config.headless:
   opts.add_argument('--headless=new')
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=opts)
```

---

## Performance & Optimization Tips

- Start small: use `--max-results 20` when testing.
- Increase `delay_between_requests` to avoid rate-limiting.
- Use headless mode for speed, but attach a visible browser when debugging element selectors.
- Cache results or run incremental updates instead of re-scraping entire queries.
- Run multiple independent worker processes with careful rate-limiting if you need parallelism.

---

## Troubleshooting

Common issues and solutions:

- "Chrome not found": install Chrome/Chromium or point the driver to the correct binary.
- WebDriver version mismatch: ensure ChromeDriver matches Chrome version or use a webdriver-manager utility.
- Empty results: try a broader query, verify selectors in `scraper/google_maps.py`, or disable headless to watch the browser.
- Timeout errors: increase `timeout` in `config.py` and/or increase `delay_between_requests`.
- Authentication / Captcha from Google: respect Terms of Service and add delays or proxies; manual intervention may be required.

If the script fails with an exception, check `logs/scraper.log` for detailed tracebacks (log file path depends on your config).

---

## API Documentation (Developer Reference)

- `scraper.google_maps.GoogleMapsScraper(config)`
  - Constructor: accept a `Config` instance
  - Methods:
   - `search_places(query: str, location: str = None) -> List[Place]` — returns parsed place objects
   - `get_place_details(place_id: str) -> Place` — fetches full details for a single place
   - `save_to_excel(results, path)` — save list of places to Excel
   - `save_to_json(results, path)` — save list of places to JSON

- `scraper.utils` contains helpers:
  - `filter_places_by_rating(results, min_rating)`
  - `sort_places_by_rating(results, descending=True)`
  - `merge_duplicate_places(results)`
  - `save_to_json(results, path)`

Place object fields (typical): `name`, `address`, `phone`, `website`, `category`, `rating`, `reviews`, `extracted_at`.

---

## Security, Legal & Ethical Notes

- Respect Google Maps' Terms of Service and local regulations.
- Do not overload Google servers — use the provided delays and rate-limits.
- This project is provided for educational and research purposes only.

---

## Contributing

Contributions welcome. Recommended workflow:

1. Fork the repo
2. Create a feature branch
3. Implement changes and add tests if applicable
4. Submit a pull request describing your changes

Please keep commits focused and add a clear description for PR reviewers.

---

## Contact

- Repository: https://github.com/ItsCxdy/google_maps_scraper
- Maintainer: talha.ovais5@gmail.com

---

## License

This project is provided as-is for educational and research purposes. Include a proper license file if you intend to redistribute.

---

If you'd like, I can also update `config.py` with clearer defaults, add examples to `bin/` for scheduled runs, or help push these changes to your GitHub remote (push will require your credentials or a configured Git credential helper).

## ✨ Features

- ✅ **No API Key Required** - Works directly with Google Maps website using web scraping
- ✅ **Dynamic Content Handling** - Uses Selenium to handle JavaScript-rendered content
- ✅ **Comprehensive Data Extraction**:
  - Business/Place Name
  - Address
  - Phone Number
  - Website
  - Category/Type
  - Rating & Review Count
  - Extraction Timestamp
- ✅ **Multiple Output Formats** - Export to Excel (.xlsx) or JSON (.json)
- ✅ **Data Filtering** - Filter by minimum rating
- ✅ **Duplicate Detection** - Automatically removes duplicate entries
- ✅ **Sorting Options** - Sort by rating, review count, or name
- ✅ **Advanced Logging** - Comprehensive logging for debugging
- ✅ **Production Ready** - Error handling and graceful failure management

## 📋 Project Structure

```
google_maps_scraper/
├── main.py                      # Entry point with CLI
├── config.py                    # Configuration settings
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── .gitignore                   # Git ignore rules
├── outputs/                     # Scraped results (auto-created)
├── logs/                        # Application logs (auto-created)
└── scraper/
    ├── __init__.py
    ├── google_maps.py           # Core scraping logic
    └── utils.py                 # Utility functions
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Chrome/Chromium browser (for Selenium WebDriver)
- pip (Python package manager)

### Step 1: Clone and Setup

```bash
# Navigate to project directory
cd google_maps_scraper

# Create virtual environment (if not already done)
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Verify Installation

```bash
python -c "from selenium import webdriver; print('✅ Selenium installed correctly')"
```

## 💻 Usage

### Basic Usage

```bash
# Search for restaurants in New York
python main.py --search "restaurants" --location "New York"

# Search for coffee shops (any location)
python main.py --search "coffee shops"
```

### Advanced Usage

```bash
# Search with custom output directory
python main.py --search "hotels" --location "London" --output results

# Limit results to 50 places
python main.py --search "banks" --location "Paris" --max-results 50

# Filter by minimum rating (4.0+)
python main.py --search "restaurants" --location "Tokyo" --min-rating 4.0

# Export to JSON format
python main.py --search "gyms" --location "Berlin" --format json

# Export to both Excel and JSON
python main.py --search "hospitals" --format both

# Sort by rating (highest first)
python main.py --search "pizza restaurants" --location "Rome" --sort-by rating

# Sort by review count
python main.py --search "museums" --location "Paris" --sort-by reviews

# Verbose output
python main.py --search "bars" --location "Barcelona" --verbose
```

### Command-Line Options

```
usage: main.py [-h] --search SEARCH [--location LOCATION] [--output OUTPUT]
               [--max-results MAX_RESULTS] [--min-rating MIN_RATING]
               [--format {xlsx,json,both}] [--sort-by {rating,reviews,name}]
               [--verbose]

Options:
  -h, --help                    Show help message
  -s, --search SEARCH           Search query (required)
  -l, --location LOCATION       Location to search in (optional)
  -o, --output OUTPUT           Output directory (default: outputs)
  -m, --max-results MAX_RESULTS Maximum results (default: 20)
  --min-rating MIN_RATING       Minimum rating filter (default: 0.0)
  -f, --format {xlsx,json,both} Output format (default: xlsx)
  --sort-by {rating,reviews,name} Sort results by...
  -v, --verbose                 Enable verbose output
```

## 📊 Output Format

### Excel (.xlsx)
The scraper generates well-formatted Excel files with:
- **Styled Headers** - Blue background with white text
- **Auto-width Columns** - Properly sized columns
- **Wrapped Text** - Long content wrapped for readability
- **Clean Data** - Organized in rows and columns

### JSON (.json)
Raw JSON format for programmatic access:
```json
[
  {
    "name": "Restaurant Name",
    "address": "123 Main St, City, State",
    "phone": "(555) 123-4567",
    "website": "https://example.com",
    "category": "Restaurant",
    "rating": "4.5",
    "reviews": "1250",
    "extracted_at": "2025-12-27 10:30:45"
  }
]
```

## 🔍 Examples

### Example 1: Search Restaurants

```bash
python main.py --search "restaurants" --location "New York" --max-results 30 --min-rating 4.0
```

**Output**: Excel file with top-rated restaurants in NYC

### Example 2: Find Coffee Shops with High Reviews

```bash
python main.py --search "coffee shops" --location "San Francisco" --sort-by reviews --max-results 50
```

**Output**: Excel file with coffee shops sorted by review count

### Example 3: Export Multiple Formats

```bash
python main.py --search "hotels" --location "Paris" --format both --max-results 25
```

**Output**: Both `google_maps_hotels_Paris_*.xlsx` and `google_maps_hotels_Paris_*.json`

## 📝 Configuration

Edit `config.py` to customize default settings:

```python
class Config:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_MAPS_API_KEY', '')
        self.default_location = 'United States'
        self.default_search_radius = 5000  # meters
        self.max_results = 20
        self.delay_between_requests = 1  # seconds
        self.timeout = 30  # seconds
        self.output_format = 'excel'
```

## ⚙️ How It Works

1. **Initialize Selenium WebDriver** - Launches headless Chrome browser
2. **Navigate to Google Maps** - Opens search URL with query and location
3. **Extract Place Elements** - Identifies and parses place listings
4. **Click & Collect Details** - Clicks on each place to fetch full information
5. **Parse & Clean Data** - Extracts relevant fields and cleans text
6. **Remove Duplicates** - Filters out duplicate entries
7. **Apply Filters** - Applies rating and other filters if specified
8. **Sort Results** - Sorts by rating, reviews, or name
9. **Export** - Saves to Excel with formatting or JSON

## 🛡️ Error Handling

The scraper includes comprehensive error handling:
- ✅ Graceful handling of network timeouts
- ✅ Missing data validation
- ✅ Duplicate detection and removal
- ✅ Invalid input detection
- ✅ Detailed error logging

## 📋 Logging

All activities are logged to `scraper.log`:
- DEBUG level logs detailed execution steps
- INFO level logs key milestones
- ERROR level logs exceptions

View logs:
```bash
tail -f scraper.log
```

## ⚠️ Important Notes

### Legal & Ethical Considerations
- ⚠️ **Use Responsibly** - Respect Google Maps' Terms of Service
- ⚠️ **Rate Limiting** - Avoid excessive requests
- ⚠️ **User-Agent** - The scraper uses a legitimate user-agent string
- ⚠️ **Headless Browser** - Uses headless Chrome to minimize detection

### Limitations
- ❌ Google Maps may detect and block excessive scraping
- ❌ Data extraction depends on HTML structure (may change)
- ❌ Does not work with VPNs/proxies in some regions
- ❌ Requires visible browser rendering (slower than API)

## 🔧 Troubleshooting

### "Chrome not found" Error
```bash
# Install Chrome/Chromium
# Windows: https://www.google.com/chrome
# macOS: brew install chromium
# Linux: sudo apt-get install chromium-browser
```

### "No results found"
1. Check spelling of search query and location
2. Try a broader search term
3. Try a different location
4. Wait and try again (may be rate-limited)

### "Timeout Error"
1. Increase timeout in `config.py`
2. Check your internet connection
3. Try with fewer max results
4. Try a simpler search query

## 📦 Dependencies

- **selenium** - Web browser automation
- **pandas** - Data manipulation
- **openpyxl** - Excel file creation
- **loguru** - Advanced logging
- **pydantic** - Data validation
- **requests** - HTTP library
- **beautifulsoup4** - HTML parsing

## 📚 Python API

### Using the Scraper Programmatically

```python
from config import Config
from scraper.google_maps import GoogleMapsScraper
from scraper import utils

# Initialize
config = Config()
config.max_results = 50
scraper = GoogleMapsScraper(config)

# Search
results = scraper.search_places("restaurants", "New York")

# Filter
results = utils.filter_places_by_rating(results, 4.0)

# Sort
results = utils.sort_places_by_rating(results, descending=True)

# Remove duplicates
results = utils.merge_duplicate_places(results)

# Save
scraper.save_to_excel(results, "output.xlsx")
utils.save_to_json(results, "output.json")
```

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is provided as-is for educational and research purposes.

## ⚡ Performance Tips

1. **Limit Results** - Start with `--max-results 20` to test
2. **Filter Early** - Use `--min-rating` to reduce data size
3. **Use Specific Locations** - More specific searches are faster
4. **Avoid Peak Hours** - Less likely to be rate-limited

## 🐛 Bug Reports

Found a bug? Please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)

## 📞 Support

For questions and support:
1. Check existing issues on GitHub
2. Review error logs in `scraper.log`
3. Try the examples provided above
4. Increase verbosity with `--verbose` flag

---

**Last Updated**: December 27, 2025  
**Version**: 1.0.0  
**Python**: 3.8+

### Command Line Interface

```bash
# Search with location
python main.py --search "coffee shops" --location "San Francisco"

# Search without location
python main.py --search "hotels"

# Custom output directory
python main.py --search "restaurants" --output "custom_output"
```

## Configuration

Edit `config.py` to customize:

- API keys
- Default search parameters
- Rate limiting settings
- Output formats
- User agent strings

## Project Structure

```
google_maps_scraper/
├── main.py                  # Entry point
├── config.py                # Configurations (API keys, default search)
├── scraper/
│   ├── __init__.py
│   ├── google_maps.py       # Core scraping logic
│   └── utils.py             # Helpers for parsing, saving to Excel, etc.
├── outputs/                 # Folder for Excel outputs
├── requirements.txt         # Dependencies
└── README.md
```

## Dependencies

- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `selenium` - Web automation (optional)
- `pandas` - Data processing
- `openpyxl` - Excel export
- `fake-useragent` - User agent rotation

## Rate Limiting

The scraper includes built-in rate limiting to avoid being blocked:

- Configurable delays between requests
- Random user agent rotation
- Timeout handling
- Error recovery mechanisms

## Output Format

Results are exported to Excel with the following columns:

- Name
- Address
- Rating
- Review Count
- Category
- Extracted Timestamp

## Legal and Ethical Considerations

- Respect Google's Terms of Service
- Use appropriate delays between requests
- Don't overload Google's servers
- Consider using official Google Maps API for commercial applications
- Be aware of local regulations regarding web scraping

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes. Please use responsibly and in compliance with applicable laws and terms of service.

## Troubleshooting

### Common Issues

- **ImportError**: Install missing dependencies with `pip install -r requirements.txt`
- **Rate limiting**: Increase delays in `config.py`
- **Empty results**: Check your search query and location
- **Excel export errors**: Ensure `openpyxl` is installed

### Getting Help

- Check the project documentation
- Review the code comments
- Test with simple search queries first
- Monitor console output for error messages

## Future Enhancements

- Google Maps API integration
- Advanced filtering and sorting
- Data visualization capabilities
- Multi-language support
- Batch processing features