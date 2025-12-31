"""
Demo Script for Testing Google Maps Scraper

This script generates sample data and tests the entire pipeline
without actually scraping Google Maps. Useful for testing output formatting.
"""

from config import Config
from scraper.google_maps import GoogleMapsScraper
from scraper import utils
import os


def generate_sample_data():
    """Generate sample place data for testing."""
    sample_places = [
        {
            'name': 'Joe\'s Pizza',
            'address': '124 Fulton St, New York, NY 10038',
            'phone': '(212) 233-2999',
            'website': 'www.joespizzanyc.com',
            'category': 'Pizza Restaurant',
            'rating': '4.5',
            'reviews': '1250',
            'extracted_at': '2025-12-27 17:30:00'
        },
        {
            'name': 'Gramercy Tavern',
            'address': '42 E 20th St, New York, NY 10003',
            'phone': '(212) 477-0777',
            'website': 'www.gramercytavern.com',
            'category': 'American Restaurant',
            'rating': '4.3',
            'reviews': '856',
            'extracted_at': '2025-12-27 17:30:00'
        },
        {
            'name': 'Balthazar',
            'address': '80 Spring St, New York, NY 10012',
            'phone': '(212) 965-1414',
            'website': 'www.balthazarny.com',
            'category': 'French Restaurant',
            'rating': '4.6',
            'reviews': '2103',
            'extracted_at': '2025-12-27 17:30:00'
        },
        {
            'name': 'Shake Shack',
            'address': '691 8th Ave, New York, NY 10036',
            'phone': '(212) 889-6600',
            'website': 'www.shakeshack.com',
            'category': 'Fast Food',
            'rating': '4.2',
            'reviews': '3456',
            'extracted_at': '2025-12-27 17:30:00'
        },
        {
            'name': 'Eleven Madison Park',
            'address': '11 Madison Ave, New York, NY 10010',
            'phone': '(212) 889-0905',
            'website': 'www.elevenmadisonpark.com',
            'category': 'Fine Dining',
            'rating': '4.7',
            'reviews': '1876',
            'extracted_at': '2025-12-27 17:30:00'
        },
        {
            'name': 'The Smith',
            'address': '1900 Broadway, New York, NY 10023',
            'phone': '(212) 496-0001',
            'website': 'www.thesmithrestaurant.com',
            'category': 'American Restaurant',
            'rating': '4.1',
            'reviews': '2234',
            'extracted_at': '2025-12-27 17:30:00'
        },
        {
            'name': 'Anemone',
            'address': '429 Amsterdam Ave, New York, NY 10024',
            'phone': '(212) 579-8850',
            'website': 'www.anemone-nyc.com',
            'category': 'Greek Restaurant',
            'rating': '4.4',
            'reviews': '567',
            'extracted_at': '2025-12-27 17:30:00'
        },
    ]
    return sample_places


def main():
    """Test the scraper output pipeline with sample data."""
    print("\n" + "="*60)
    print("🧪 GOOGLE MAPS SCRAPER - DEMO/TEST MODE")
    print("="*60)
    print("📝 This script tests the output pipeline with sample data\n")
    
    # Generate sample data
    places = generate_sample_data()
    print(f"✅ Generated {len(places)} sample restaurants\n")
    
    # Create output directory
    output_dir = utils.ensure_output_directory('outputs')
    
    # Filter by rating
    print("Applying filters...")
    places_high_rated = utils.filter_places_by_rating(places, 4.3)
    print(f"  📊 Filtered to {len(places_high_rated)} restaurants with 4.3+ rating\n")
    
    # Sort by rating
    places_sorted = utils.sort_places_by_rating(places_high_rated, descending=True)
    
    # Remove duplicates
    places_unique = utils.merge_duplicate_places(places_sorted)
    print(f"  🔄 After deduplication: {len(places_unique)} restaurants\n")
    
    # Create scraper instance for Excel export
    config = Config()
    scraper = GoogleMapsScraper(config)
    
    # Generate output filenames
    base_filename = utils.create_output_filename("test_restaurants", "New York")
    base_path = os.path.join(output_dir, base_filename.replace('.xlsx', ''))
    
    # Export to Excel
    print("Exporting results...")
    xlsx_file = f"{base_path}.xlsx"
    scraper.save_to_excel(places_unique, xlsx_file)
    
    # Export to JSON
    json_file = f"{base_path}.json"
    utils.save_to_json(places_unique, json_file)
    
    # Display results
    print("\n" + "="*60)
    print("📊 RESULTS SUMMARY")
    print("="*60)
    
    for idx, place in enumerate(places_unique, 1):
        print(f"\n{idx}. {place['name']}")
        print(f"   📍 {place['address']}")
        print(f"   📞 {place['phone']}")
        if float(place.get('rating', 0)) > 0:
            print(f"   ⭐ Rating: {place['rating']} ({place.get('reviews', 0)} reviews)")
        if place.get('website'):
            print(f"   🌐 {place['website']}")
    
    print("\n" + "="*60)
    print("✅ DEMO COMPLETE!")
    print(f"✅ Excel file: {xlsx_file}")
    print(f"✅ JSON file: {json_file}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
