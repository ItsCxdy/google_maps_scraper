"""
Utility Functions Module

This module contains helper functions for parsing data, saving to Excel,
and other utility operations used throughout the scraper.
"""

import re
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from loguru import logger


def clean_text(text: str) -> str:
    """
    Clean and normalize text by removing extra whitespace and special characters.
    
    Args:
        text: Raw text string
        
    Returns:
        Cleaned text string
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text


def extract_rating(rating_text: str) -> float:
    """
    Extract numeric rating from rating text.
    
    Args:
        rating_text: Text containing rating (e.g., "4.5 stars")
        
    Returns:
        Numeric rating value
    """
    if not rating_text:
        return 0.0
    
    try:
        # Extract numeric value using regex
        match = re.search(r'(\d+\.?\d*)', str(rating_text))
        if match:
            return float(match.group(1))
    except ValueError:
        pass
    
    return 0.0


def extract_review_count(review_text: str) -> int:
    """
    Extract numeric review count from review text.
    
    Args:
        review_text: Text containing review count (e.g., "1,234 reviews")
        
    Returns:
        Numeric review count
    """
    if not review_text:
        return 0
    
    try:
        # Remove commas and extract numeric value
        cleaned = re.sub(r'[^\d]', '', str(review_text))
        if cleaned:
            return int(cleaned)
    except ValueError:
        pass
    
    return 0


def parse_address(address: str) -> Dict[str, str]:
    """
    Parse address string into components.
    
    Args:
        address: Full address string
        
    Returns:
        Dictionary with address components (street, city, state, zip, country)
    """
    if not address:
        return {
            'street': '',
            'city': '',
            'state': '',
            'zip': '',
            'country': ''
        }
    
    # Simple parsing - actual implementation would be more sophisticated
    parts = [p.strip() for p in address.split(',')]
    
    result = {
        'street': parts[0] if len(parts) > 0 else '',
        'city': parts[1] if len(parts) > 1 else '',
        'state': parts[2] if len(parts) > 2 else '',
        'zip': '',
        'country': parts[-1] if len(parts) > 0 else ''
    }
    
    return result


def format_phone_number(phone: str) -> str:
    """
    Format phone number to standard format.
    
    Args:
        phone: Raw phone number string
        
    Returns:
        Formatted phone number
    """
    if not phone:
        return ""
    
    # Remove all non-digit characters
    digits = re.sub(r'[^\d]', '', str(phone))
    
    # Format as (XXX) XXX-XXXX for US numbers
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) > 0:
        return f"+{digits}"
    
    return phone


def validate_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email: Email address string
        
    Returns:
        True if valid, False otherwise
    """
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, str(email)))


def get_timestamp() -> str:
    """
    Get current timestamp in ISO format.
    
    Returns:
        Current timestamp string
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def create_output_filename(search_query: str, location: str = None) -> str:
    """
    Create a unique filename for output based on search query and timestamp.
    
    Args:
        search_query: The search query string
        location: Optional location string
        
    Returns:
        Formatted filename for Excel output
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if location:
        filename = f"google_maps_{search_query}_{location}_{timestamp}.xlsx"
    else:
        filename = f"google_maps_{search_query}_{timestamp}.xlsx"
    
    # Clean filename of special characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    return filename


def ensure_output_directory(directory: str = 'outputs') -> str:
    """
    Ensure output directory exists, create if it doesn't.
    
    Args:
        directory: Directory path
        
    Returns:
        Absolute path to directory
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"Created output directory: {directory}")
    return directory


def save_to_json(data: List[Dict[str, Any]], filename: str) -> None:
    """
    Save data to JSON file.
    
    Args:
        data: List of dictionaries to save
        filename: Output JSON filename
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Data saved to {filename}")
        print(f"✅ Data saved to {filename}")
    except Exception as e:
        logger.error(f"Error saving to JSON: {e}")
        print(f"❌ Error saving to JSON: {e}")


def load_from_json(filename: str) -> List[Dict[str, Any]]:
    """
    Load data from JSON file.
    
    Args:
        filename: JSON filename to load
        
    Returns:
        List of dictionaries
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"File not found: {filename}")
        print(f"⚠️ File not found: {filename}")
        return []
    except Exception as e:
        logger.error(f"Error loading from JSON: {e}")
        print(f"❌ Error loading from JSON: {e}")
        return []


def merge_duplicate_places(places: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Merge duplicate places based on name and address.
    
    Args:
        places: List of place dictionaries
        
    Returns:
        List of unique places
    """
    seen = set()
    unique_places = []
    
    for place in places:
        # Create a unique key based on name and address
        name = clean_text(place.get('name', ''))
        address = clean_text(place.get('address', ''))
        key = f"{name}_{address}"
        
        if key and key not in seen:
            seen.add(key)
            unique_places.append(place)
    
    return unique_places


def filter_places_by_rating(places: List[Dict[str, Any]], min_rating: float) -> List[Dict[str, Any]]:
    """
    Filter places by minimum rating.
    
    Args:
        places: List of place dictionaries
        min_rating: Minimum rating threshold
        
    Returns:
        Filtered list of places
    """
    filtered = []
    for place in places:
        try:
            rating = float(place.get('rating', 0))
            if rating >= min_rating:
                filtered.append(place)
        except (ValueError, TypeError):
            pass
    
    return filtered


def sort_places_by_rating(places: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    """
    Sort places by rating.
    
    Args:
        places: List of place dictionaries
        descending: Sort order (True for descending, False for ascending)
        
    Returns:
        Sorted list of places
    """
    try:
        return sorted(
            places,
            key=lambda x: float(x.get('rating', 0)),
            reverse=descending
        )
    except Exception as e:
        logger.warning(f"Error sorting by rating: {e}")
        return places


def sort_places_by_reviews(places: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    """
    Sort places by number of reviews.
    
    Args:
        places: List of place dictionaries
        descending: Sort order (True for descending, False for ascending)
        
    Returns:
        Sorted list of places
    """
    try:
        return sorted(
            places,
            key=lambda x: int(x.get('reviews', 0)),
            reverse=descending
        )
    except Exception as e:
        logger.warning(f"Error sorting by reviews: {e}")
        return places