"""
Google Maps Scraper - Core Logic (FIXED v5)

Updates:
1. URL Cleaning: Extracts the real website from Google's redirect links.
2. Robust Extraction: Maintains the detail panel clicking and header checks.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import List, Dict, Any, Optional
import time
import re
from urllib.parse import urlparse, parse_qs  # Added for URL cleaning
from loguru import logger
from config import Config


class GoogleMapsScraper:
    def __init__(self, config: Config):
        self.config = config
        self.driver = None
        self.wait = None
        logger.info("GoogleMapsScraper initialized")
    
    def _initialize_driver(self):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument(f'user-agent={self.config.get_user_agent()}')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument("--window-size=1920,1080")
            
            self.driver = webdriver.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, 15)
            logger.info("Chrome WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise
    
    def _close_driver(self):
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver closed")
    
    def search_places(self, query: str, location: str = None) -> List[Dict[str, Any]]:
        try:
            self._initialize_driver()
            search_query = f"{query} in {location}" if location else query
            search_url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
            
            logger.info(f"Searching for: {search_query}")
            self.driver.get(search_url)
            
            try:
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]')))
            except TimeoutException:
                logger.warning("Results feed not detected.")

            return self._extract_places()
        except Exception as e:
            logger.error(f"Error during search: {e}")
            return []
        finally:
            self._close_driver()
    
    def _scroll_page(self):
        try:
            scrollable_div = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]')))
            for _ in range(3):
                self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
                time.sleep(2)
        except: pass

    def _extract_places(self) -> List[Dict[str, Any]]:
        places = []
        self._scroll_page()
        
        selector = 'a.hfpxzc'
        
        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            total_to_process = min(len(elements), self.config.get_max_results())
            logger.info(f"Found {len(elements)} results. Extracting details...")

            for i in range(total_to_process):
                try:
                    current_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if i >= len(current_elements): break
                    
                    self.driver.execute_script("arguments[0].click();", current_elements[i])
                    time.sleep(3)

                    place_info = self._extract_side_panel_info()
                    if place_info:
                        if place_info['name'].lower() != "results":
                            places.append(place_info)
                            logger.info(f"Extracted: {place_info['name']}")
                except Exception as e:
                    logger.debug(f"Error at index {i}: {e}")
                    
        except Exception as e:
            logger.error(f"Extraction failed: {e}")
        
        return places
    
    def _extract_side_panel_info(self) -> Optional[Dict[str, Any]]:
        try:
            name_el = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.DUwDvf')))
            
            data = {
                'name': name_el.text,
                'address': "N/A",
                'phone': "N/A",
                'website': "N/A",
                'category': "N/A",
                'rating': "0.0",
                'reviews': "0",
                'extracted_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }

            # Rating and Reviews
            try:
                # Updated rating selector for clarity
                rating_container = self.driver.find_element(By.CSS_SELECTOR, 'div.F7k0ve')
                data['rating'] = rating_container.text.split('\n')[0].strip()
                review_text = self.driver.find_element(By.CSS_SELECTOR, 'span.fontBodyMedium > span > span').text
                data['reviews'] = review_text.replace('(', '').replace(')', '').replace(',', '').strip()
            except: pass

            # Category
            try:
                data['category'] = self.driver.find_element(By.CSS_SELECTOR, 'button.DkEaL').text
            except: pass

            # Address
            try:
                data['address'] = self.driver.find_element(By.CSS_SELECTOR, 'button[data-item-id="address"]').get_attribute('aria-label').replace('Address: ', '')
            except: pass

            # Phone
            try:
                phone_el = self.driver.find_element(By.CSS_SELECTOR, 'button[data-item-id^="phone:tel:"]')
                data['phone'] = phone_el.get_attribute('aria-label').replace('Phone: ', '')
            except: pass

            # Website with URL CLEANING
            try:
                raw_url = self.driver.find_element(By.CSS_SELECTOR, 'a[data-item-id="authority"]').get_attribute('href')
                if "google.com/url?" in raw_url:
                    parsed_url = urlparse(raw_url)
                    # Extract the 'q' parameter which contains the real website
                    clean_url = parse_qs(parsed_url.query).get('q', [raw_url])[0]
                    data['website'] = clean_url
                else:
                    data['website'] = raw_url
            except: pass

            return data
            
        except Exception as e:
            logger.debug(f"Side panel extraction failed: {e}")
            return None

    def save_to_excel(self, places: List[Dict[str, Any]], filename: str) -> None:
        try:
            import pandas as pd
            if not places:
                logger.warning("No places to save.")
                return

            df = pd.DataFrame(places)
            if 'name' in df.columns:
                df = df[df['name'] != 'Sponsored']
                df = df[df['name'].str.lower() != 'results']
            
            df.to_excel(filename, index=False)
            logger.info(f"Successfully saved {len(df)} records to {filename}")
        except Exception as e:
            logger.error(f"Excel save error: {e}")