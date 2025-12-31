#!/usr/bin/env python3
"""
Helper script to update CSS selectors in the Google Maps scraper.

This script provides an interactive way to update selectors without manually
editing the Python file. It helps identify and test new selectors.

Usage:
    python update_selectors.py
"""

import sys
from pathlib import Path


def update_selectors():
    """Interactive selector updater."""
    
    print("\n" + "=" * 70)
    print("🔍 Google Maps Scraper - CSS Selector Update Tool".center(70))
    print("=" * 70)
    
    print("\n📖 INSTRUCTIONS:")
    print("-" * 70)
    print("1. Open https://www.google.com/maps in Chrome")
    print("2. Search for something like: 'restaurants in New York'")
    print("3. Press F12 to open Developer Tools")
    print("4. Right-click on a place listing → Inspect")
    print("5. Right-click the element → Copy selector")
    print("6. Paste the selector below")
    print("-" * 70)
    
    # Get new place selectors
    print("\n📍 PLACE LISTING SELECTORS")
    print("-" * 70)
    print("These select individual restaurant/place items in the list.")
    print("You need at least 1 selector. Enter multiple for fallbacks.\n")
    
    place_selectors = []
    count = 1
    while True:
        selector = input(f"Selector #{count} (or press Enter to skip): ").strip()
        if not selector:
            if place_selectors:
                break
            if count > 1:
                break
            print("⚠️  Please enter at least one selector!")
            continue
        place_selectors.append(selector)
        count += 1
    
    if not place_selectors:
        print("❌ No place selectors entered. Aborting.")
        return
    
    # Get new scroll selectors
    print("\n🔄 SCROLL CONTAINER SELECTORS")
    print("-" * 70)
    print("These select the container that holds the place listings.")
    print("This is the element that scrolls to load more results.\n")
    
    scroll_selectors = []
    count = 1
    while True:
        selector = input(f"Selector #{count} (or press Enter to skip): ").strip()
        if not selector:
            if scroll_selectors:
                break
            if count > 1:
                break
            print("⚠️  Please enter at least one selector!")
            continue
        scroll_selectors.append(selector)
        count += 1
    
    if not scroll_selectors:
        print("⚠️  No scroll selectors entered. Will use fallback (window scroll).")
    
    # Confirm before updating
    print("\n" + "=" * 70)
    print("📋 REVIEW YOUR SELECTORS")
    print("=" * 70)
    
    print("\n✅ Place Selectors:")
    for i, sel in enumerate(place_selectors, 1):
        print(f"   {i}. {sel}")
    
    if scroll_selectors:
        print("\n✅ Scroll Selectors:")
        for i, sel in enumerate(scroll_selectors, 1):
            print(f"   {i}. {sel}")
    else:
        print("\n⚠️  No scroll selectors (will use window.scrollBy fallback)")
    
    confirm = input("\n🚀 Update the code? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Cancelled.")
        return
    
    # Update the file
    try:
        scraper_file = Path('scraper/google_maps.py')
        
        if not scraper_file.exists():
            print(f"❌ Error: {scraper_file} not found!")
            print("   Make sure you're in the project root directory.")
            return
        
        with open(scraper_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content  # Keep original for comparison
        
        # Update place selectors (around line 114)
        # Build the new selectors list
        place_str = "[\n"
        for sel in place_selectors:
            place_str += f"                '{sel}',\n"
        place_str = place_str.rstrip(',\n') + "\n            ]"
        
        # Find and replace place selectors
        old_place = """    selectors = [
                'div[role="listitem"]',
                'div[data-index]',
                'div.lI9Ife',
                'div[jsname]'
            ]"""
        
        new_place = f"""    selectors = {place_str}"""
        
        if old_place in content:
            content = content.replace(old_place, new_place)
            print("✅ Updated place selectors")
        else:
            print("⚠️  Could not find place selector section (may have been modified)")
        
        # Update scroll selectors (around line 158)
        if scroll_selectors:
            scroll_str = "[\n"
            for sel in scroll_selectors:
                scroll_str += f"                '{sel}',\n"
            scroll_str = scroll_str.rstrip(',\n') + "\n            ]"
            
            old_scroll = """            selectors = [
                'div[role="feed"]',
                'div[role="list"]',
                'div.m6QErb',
                'div[jsname="yUQnFb"]'
            ]"""
            
            new_scroll = f"""            selectors = {scroll_str}"""
            
            if old_scroll in content:
                content = content.replace(old_scroll, new_scroll)
                print("✅ Updated scroll selectors")
            else:
                print("⚠️  Could not find scroll selector section (may have been modified)")
        
        # Check if anything changed
        if content == original_content:
            print("\n❌ No changes made. Selectors may have been moved or modified.")
            print("   Try manually editing: scraper/google_maps.py")
            print("   Around line 114 and line 158")
            return
        
        # Write back
        with open(scraper_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Success message
        print("\n" + "=" * 70)
        print("✨ SUCCESS! Selectors updated!".center(70))
        print("=" * 70)
        
        print("\n📝 Summary:")
        print(f"   • Place selectors: {len(place_selectors)} selector(s)")
        print(f"   • Scroll selectors: {len(scroll_selectors)} selector(s)")
        
        print("\n🚀 Next Steps:")
        print("   1. Test with demo first: python test_demo.py")
        print("   2. Try live scraping: python main.py --search restaurants --location \"New York\" --verbose")
        print("   3. Check logs if needed: cat scraper.log")
        
        print("\n💡 Tips:")
        print("   • Use --verbose flag to see detailed selector attempts")
        print("   • Check scraper.log for what selectors are found")
        print("   • If 0 results, may need to update the regex in _extract_place_info()")
        
    except Exception as e:
        print(f"\n❌ Error updating file: {e}")
        print("   Please update manually: scraper/google_maps.py")
        return


def test_selector_interactive():
    """Test a selector by actually scraping with it."""
    
    print("\n" + "=" * 70)
    print("🧪 Selector Tester (Coming soon)".center(70))
    print("=" * 70)
    print("\nFor now, use this process:")
    print("   1. Create a test file with your selector")
    print("   2. Run: python main.py --search restaurants --location 'New York' --verbose")
    print("   3. Check the output to see if selectors are found")


def main():
    """Main entry point."""
    
    try:
        update_selectors()
        print("\n✅ Done!\n")
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
