import argparse
from loguru import logger
from config import Config
from scraper.google_maps import GoogleMapsScraper
from scraper import utils


def main():
    parser = argparse.ArgumentParser(description="Google Maps Scraper")

    parser.add_argument("--search", required=True)
    parser.add_argument("--location")
    parser.add_argument("--max-results", type=int, default=20)
    parser.add_argument("--min-rating", type=float, default=0)

    # 🔥 NEW FLAGS
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--delay", type=int, default=2)
    parser.add_argument("--category-filter")

    args = parser.parse_args()

    config = Config()
    config.max_results = args.max_results
    config.delay_between_requests = args.delay
    config.headless = args.headless
    config.category_filter = args.category_filter

    scraper = GoogleMapsScraper(config)

    results = scraper.search_places(args.search, args.location)
    if not results:
        print("No results found")
        return

    results = utils.merge_duplicate_places(results)

    if args.min_rating:
        results = utils.filter_places_by_rating(results, args.min_rating)

    out_dir = utils.ensure_output_directory()
    filename = utils.create_output_filename(args.search, args.location)
    scraper.save_to_excel(results, f"{out_dir}/{filename}")

    print(f"✅ Saved {len(results)} places")


if __name__ == "__main__":
    main()
