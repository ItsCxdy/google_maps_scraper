"""
Google Maps Scraper - Entry Point

This script serves as the main entry point for the Google Maps scraper application.
It initializes the scraper and coordinates the scraping process based on user input.
"""

import sys
import os
import argparse
from pathlib import Path
from loguru import logger
from config import Config
from scraper.google_maps import GoogleMapsScraper
from scraper import utils


def setup_logging(log_file: str = 'scraper.log'):
    """Setup logging configuration."""
    # Remove default handler
    logger.remove()
    
    # Add console handler
    logger.add(
        sys.stderr,
        format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level="INFO"
    )
    
    # Add file handler
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
        rotation="10 MB"
    )


def main():
    """Main function to run the Google Maps scraper."""
    setup_logging()
    
    parser = argparse.ArgumentParser(
        description='🗺️  Google Maps Scraper - Extract business information from Google Maps',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --search "restaurants" --location "New York"
  python main.py --search "coffee shops" --location "San Francisco" --output results
  python main.py --search "hospitals" --max-results 50
        """
    )
    
    parser.add_argument(
        '--search', '-s',
        type=str,
        required=True,
        help='Search query (e.g., "restaurants", "hotels", "coffee shops")'
    )
    parser.add_argument(
        '--location', '-l',
        type=str,
        default=None,
        help='Location to search in (e.g., "New York", "San Francisco")'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='outputs',
        help='Output directory for results (default: outputs)'
    )
    parser.add_argument(
        '--max-results', '-m',
        type=int,
        default=20,
        help='Maximum number of results to scrape (default: 20)'
    )
    parser.add_argument(
        '--min-rating',
        type=float,
        default=0.0,
        help='Minimum rating filter (default: 0.0)'
    )
    parser.add_argument(
        '--format', '-f',
        type=str,
        choices=['xlsx', 'json', 'both'],
        default='xlsx',
        help='Output format (default: xlsx)'
    )
    parser.add_argument(
        '--sort-by',
        type=str,
        choices=['rating', 'reviews', 'name'],
        default=None,
        help='Sort results by rating, reviews, or name'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = utils.ensure_output_directory(args.output)
    
    # Initialize configuration
    config = Config()
    config.max_results = args.max_results
    
    logger.info(f"Starting Google Maps scraper for: {args.search}")
    if args.location:
        logger.info(f"Location: {args.location}")
    
    print("\n" + "="*60)
    print("🗺️  GOOGLE MAPS SCRAPER")
    print("="*60)
    print(f"📍 Search Query: {args.search}")
    if args.location:
        print(f"📍 Location: {args.location}")
    print(f"📊 Max Results: {args.max_results}")
    print(f"⏱️  Please wait... this may take a few minutes...")
    print("="*60 + "\n")
    
    # Initialize scraper
    scraper = GoogleMapsScraper(config)
    
    # Perform scraping
    try:
        # Search for places
        results = scraper.search_places(args.search, args.location)
        
        if not results:
            print("⚠️  No results found. Please try a different search query or location.")
            logger.warning(f"No results found for: {args.search} in {args.location}")
            return
        
        print(f"✅ Found {len(results)} places\n")
        logger.info(f"Found {len(results)} places")
        
        # Apply filters
        if args.min_rating > 0:
            original_count = len(results)
            results = utils.filter_places_by_rating(results, args.min_rating)
            print(f"📊 Filtered to {len(results)} places with rating >= {args.min_rating}")
            logger.info(f"Filtered from {original_count} to {len(results)} places")
        
        # Remove duplicates
        results = utils.merge_duplicate_places(results)
        print(f"🔄 After removing duplicates: {len(results)} places\n")
        
        # Sort results
        if args.sort_by == 'rating':
            results = utils.sort_places_by_rating(results)
            print("📈 Sorted by rating (highest first)\n")
        elif args.sort_by == 'reviews':
            results = utils.sort_places_by_reviews(results)
            print("📈 Sorted by review count (highest first)\n")
        
        # Generate output filenames
        base_filename = utils.create_output_filename(args.search, args.location)
        base_path = os.path.join(output_dir, base_filename.replace('.xlsx', ''))
        
        # Save results
        if args.format in ['xlsx', 'both']:
            xlsx_file = f"{base_path}.xlsx"
            scraper.save_to_excel(results, xlsx_file)
        
        if args.format in ['json', 'both']:
            json_file = f"{base_path}.json"
            utils.save_to_json(results, json_file)
        
        # Print summary
        print("="*60)
        print("📊 RESULTS SUMMARY")
        print("="*60)
        if results:
            # Print first few results
            for idx, place in enumerate(results[:5], 1):
                print(f"\n{idx}. {place.get('name', 'N/A')}")
                if place.get('address'):
                    print(f"   📍 {place['address']}")
                if place.get('phone'):
                    print(f"   📞 {place['phone']}")
                if place.get('rating') and float(place.get('rating', 0)) > 0:
                    print(f"   ⭐ Rating: {place['rating']} ({place.get('reviews', 0)} reviews)")
        
        if len(results) > 5:
            print(f"\n... and {len(results) - 5} more places")
        
        print("\n" + "="*60)
        logger.info("Scraping completed successfully")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user")
        logger.warning("Scraping interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error during scraping: {e}")
        logger.error(f"Error during scraping: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()