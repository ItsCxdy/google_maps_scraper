from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs
import time
from loguru import logger

from config import Config
from scraper.utils import safe_extract


class GoogleMapsScraper:
    def __init__(self, config: Config):
        self.config = config
        self.driver = None
        self.wait = None

    def _initialize_driver(self):
        options = webdriver.ChromeOptions()

        if self.config.headless:
            options.add_argument("--headless=new")

        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--window-size=1920,1080")
        options.add_argument(f"user-agent={self.config.get_user_agent()}")

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, self.config.timeout)

    def _close_driver(self):
        if self.driver:
            self.driver.quit()

    def search_places(self, query, location=None):
        try:
            self._initialize_driver()
            search = f"{query} in {location}" if location else query
            url = f"https://www.google.com/maps/search/{search.replace(' ', '+')}"
            self.driver.get(url)

            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]')))
            time.sleep(2)
            return self._extract_places()
        finally:
            self._close_driver()

    def _scroll(self):
        feed = self.driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
        for _ in range(3):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", feed)
            time.sleep(2)

    def _extract_places(self):
        self._scroll()
        results = []

        cards = self.driver.find_elements(By.CSS_SELECTOR, "a.hfpxzc")
        limit = min(len(cards), self.config.max_results)

        for i in range(limit):
            try:
                cards = self.driver.find_elements(By.CSS_SELECTOR, "a.hfpxzc")
                self.driver.execute_script("arguments[0].click();", cards[i])
                time.sleep(self.config.delay_between_requests)

                data = self._extract_side_panel()
                if not data:
                    continue

                if self.config.category_filter:
                    if self.config.category_filter.lower() not in data["category"].lower():
                        continue

                results.append(data)
                logger.info(f"Extracted {data['name']}")

            except Exception as e:
                logger.debug(e)

        return results

    def _extract_side_panel(self):
        try:
            name = safe_extract(self.driver, [
                "h1.DUwDvf",
                "div.fontHeadlineLarge",
                "h1.text-headline-1"
            ])

            if name in ("N/A", "Results"):
                return None

            category = safe_extract(self.driver, ["button.DkEaL"])
            address = safe_extract(
                self.driver,
                ['button[data-item-id="address"]'],
                attr="aria-label"
            ).replace("Address: ", "")

            phone = safe_extract(
                self.driver,
                ['button[data-item-id^="phone"]'],
                attr="aria-label"
            ).replace("Phone: ", "")

            raw_url = safe_extract(
                self.driver,
                ['a[data-item-id="authority"]'],
                attr="href"
            )

            website = "N/A"
            if "google.com/url?" in raw_url:
                parsed = urlparse(raw_url)
                website = parse_qs(parsed.query).get("q", ["N/A"])[0]
            else:
                website = raw_url

            rating = safe_extract(self.driver, ["div.F7k0ve"])
            reviews = safe_extract(self.driver, ["span.fontBodyMedium > span > span"])

            return {
                "name": name,
                "category": category,
                "address": address,
                "phone": phone,
                "website": website,
                "rating": rating,
                "reviews": reviews,
                "extracted_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            }

        except:
            return None
    def save_to_excel(self, places, filename):
        """
        Save extracted places to Excel file.
        """
        try:
            import pandas as pd

            if not places:
                logger.warning("No places to save.")
                return

            df = pd.DataFrame(places)

            # Safety cleanup
            if "name" in df.columns:
                df = df[df["name"].str.lower() != "results"]
                df = df[df["name"].str.lower() != "sponsored"]

            df.to_excel(filename, index=False)
            logger.info(f"Saved {len(df)} records to {filename}")

        except Exception as e:
            logger.error(f"Excel save failed: {e}")
