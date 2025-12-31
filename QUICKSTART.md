# Google Maps Scraper - Quick Start Guide

## 📋 Prerequisites

- Windows OS with Python 3.14+ installed
- Virtual environment activated
- All dependencies installed from requirements.txt

## 🚀 Quick Commands

### 1. Activate Virtual Environment

```powershell
# Windows PowerShell
venv\Scripts\activate

# Windows Command Prompt
venv\Scripts\activate.bat
```

### 2. Run Demo (Immediate Results with Sample Data)

```powershell
python test_demo.py
```

**Result**: Generates sample restaurant data, filters it, and exports to Excel + JSON
**Output Files**: Check `outputs/` folder

### 3. Search Google Maps (Live Scraping)

```powershell
# Basic search
python main.py --search "restaurants" --location "New York"

# With filters
python main.py --search "coffee shops" --location "Boston" --max-results 15 --min-rating 4.0

# With sorting
python main.py --search "hotels" --location "Las Vegas" --sort-by reviews --format both

# Verbose mode (see all details)
python main.py --search "pizza" --location "Chicago" --verbose
```

### 4. View Help

```powershell
python main.py --help
```

---

## 📊 Output Files

After running commands, check the `outputs/` folder for:

- **Excel Files** (.xlsx) - With styled headers and formatting
- **JSON Files** (.json) - Machine-readable format

Example filenames:
```
google_maps_results_New_York_20241227_120000.xlsx
google_maps_results_New_York_20241227_120000.json
```

---

## 🔍 View Results

### Check Excel File

```powershell
python verify_excel.py
```

### View Logs

```powershell
# See last 20 lines of log
Get-Content scraper.log -Tail 20

# Or open in Notepad
notepad scraper.log
```

---

## 📝 Command Examples

### Example 1: Find Highly-Rated Restaurants

```powershell
python main.py --search "restaurants" --location "Bareilly" --min-rating 4.5 --max-results 20
```

### Example 2: Compare Pizza Places by Reviews

```powershell
python main.py --search "pizza" --location "Chicago" --sort-by reviews --max-results 10
```

### Example 3: Export Multiple Formats

```powershell
python main.py --search "hotels" --location "Los Angeles" --format both --max-results 15
```

### Example 4: Debug Mode

```powershell
python main.py --search "coffee" --location "Seattle" --verbose --max-results 5
```

---

## ✅ Expected Output

When you run a search, you should see:

```
🔍 Searching for 'restaurants' in 'New York'...
⏳ Loading page... (may take 10-20 seconds)
📍 Found 45 places on Google Maps
🔄 Processing results...
✅ Found 42 unique places
📊 Filtered to 35 places with rating >= 0.0
📝 Sorting by: rating (descending)
💾 Exported results to: outputs/google_maps_results_New_York_20241227_120000.xlsx
✨ Done!
```

---

## ❌ Troubleshooting

### "Found 0 places" Error

This happens when Google Maps HTML selectors have changed. Solution:

1. Open Chrome
2. Go to Google Maps
3. Search for a place type manually
4. Press F12 (Developer Tools)
5. Right-click on a place listing → Inspect
6. Note the HTML element structure
7. Update CSS selectors in `scraper/google_maps.py` (around line 150)
8. Retry the command

### "Chrome driver not found" Error

This shouldn't happen if Selenium is properly installed. Try:

```powershell
pip install --upgrade selenium
```

### Virtual Environment Not Activated

You'll see `(venv)` at the start of your prompt if it's activated:

```
(venv) PS E:\Codes\google_maps_scraper>
```

If not, activate it:

```powershell
venv\Scripts\activate
```

### Dependencies Not Installed

```powershell
pip install -r requirements.txt
```

---

## 📚 More Information

- Full documentation: See `README.md`
- Project status: See `SETUP_COMPLETE.md`
- Completion report: See `PROJECT_COMPLETION_REPORT.md`

---

## 🎯 Common Workflows

### Workflow 1: Test the System with Demo Data
```powershell
# Step 1: Activate environment
venv\Scripts\activate

# Step 2: Run demo
python test_demo.py

# Step 3: Check output
python verify_excel.py
```

### Workflow 2: Live Scraping with Filtering
```powershell
# Activate
venv\Scripts\activate

# Search and filter
python main.py --search "restaurants" --location "New York" --min-rating 4.3 --max-results 20

# Check results
Get-ChildItem outputs/ | Sort-Object LastWriteTime -Descending | Select-Object -First 1
```

### Workflow 3: Compare Multiple Locations
```powershell
# Activate
venv\Scripts\activate

# Search New York
python main.py --search "coffee" --location "New York" --sort-by reviews > ny_results.txt

# Search Chicago
python main.py --search "coffee" --location "Chicago" --sort-by reviews > chicago_results.txt

# View and compare
Write-Host "New York:"; Get-Content ny_results.txt
Write-Host "`nChicago:"; Get-Content chicago_results.txt
```

---

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Maximum results to fetch
MAX_RESULTS = 20

# Timeout for Selenium operations
TIMEOUT = 15

# Output format (xlsx, json, or both)
OUTPUT_FORMAT = "xlsx"

# User agent string
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
```

---

## 📞 Support

If you encounter issues:

1. **Check the logs**: `Get-Content scraper.log`
2. **Enable verbose mode**: Add `--verbose` flag
3. **Review documentation**: See README.md
4. **Check configuration**: Edit config.py

---

**Last Updated**: December 27, 2024  
**Python Version**: 3.14.2  
**Selenium Version**: 4.39
