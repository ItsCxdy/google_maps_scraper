"""
Utility Functions Module
"""

import re
import json
import os
from typing import List, Dict, Any
from datetime import datetime
from loguru import logger
from selenium.webdriver.common.by import By


def clean_text(text: str) -> str:
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()


def safe_extract(driver, selectors, attr: str = None) -> str:
    """
    Google-safe extractor with selector fallbacks.
    """
    for selector in selectors:
        try:
            el = driver.find_element(By.CSS_SELECTOR, selector)
            value = el.get_attribute(attr) if attr else el.text
            if value and value.strip():
                return value.strip()
        except:
            continue
    return "N/A"


def extract_rating(text: str) -> float:
    try:
        match = re.search(r'(\d+\.?\d*)', text)
        return float(match.group(1)) if match else 0.0
    except:
        return 0.0


def extract_review_count(text: str) -> int:
    try:
        return int(re.sub(r'[^\d]', '', text))
    except:
        return 0


def ensure_output_directory(directory: str = "outputs") -> str:
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"Created directory {directory}")
    return directory


def create_output_filename(search: str, location: str = None) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = f"{search}_{location}_{ts}" if location else f"{search}_{ts}"
    return re.sub(r'[<>:"/\\|?*]', "_", name) + ".xlsx"


def save_to_json(data: List[Dict[str, Any]], filename: str):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def merge_duplicate_places(places: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    unique = []
    for p in places:
        key = (p.get("name"), p.get("address"))
        if key not in seen:
            seen.add(key)
            unique.append(p)
    return unique


def filter_places_by_rating(places, min_rating):
    filtered = []

    for p in places:
        rating = normalize_rating(p.get("rating", ""))
        if rating is None:
            continue

        if rating >= min_rating:
            filtered.append(p)

    return filtered


def normalize_rating(rating_raw: str) -> float | None:
    """
    Extract the first valid numeric rating from text.
    Examples:
      "4.6\n2,345 reviews" -> 4.6
      "4.2 stars"         -> 4.2
      "N/A"               -> None
    """
    if not rating_raw:
        return None

    match = re.search(r"\b\d\.\d\b", rating_raw)
    if not match:
        return None

    try:
        return float(match.group())
    except ValueError:
        return None


def sort_places_by_rating(places):
    return sorted(places, key=lambda x: float(x.get("rating", 0)), reverse=True)


def sort_places_by_reviews(places):
    return sorted(places, key=lambda x: int(x.get("reviews", 0)), reverse=True)
