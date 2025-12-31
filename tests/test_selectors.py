import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scraper.utils import safe_extract


@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def open_first_place(driver):
    """
    Open Google Maps search and click first result
    (this guarantees the side panel opens)
    """
    driver.get("https://www.google.com/maps/search/Gramercy+Tavern/")
    wait = WebDriverWait(driver, 20)

    # Wait for results list
    first_result = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.hfpxzc"))
    )

    driver.execute_script("arguments[0].click();", first_result)

    # Wait for place name to appear in side panel
    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "h1.DUwDvf, div.fontHeadlineLarge")
        )
    )


def test_place_name_selector(driver):
    open_first_place(driver)

    name = safe_extract(driver, [
        "h1.DUwDvf",
        "div.fontHeadlineLarge",
        "h1.text-headline-1"
    ])

    assert name != "N/A"
    assert len(name) > 3


def test_category_selector(driver):
    category = safe_extract(driver, [
        "button.DkEaL",
        "div.fontBodyMedium"
    ])

    assert category != "N/A"


def test_address_selector(driver):
    address = safe_extract(
        driver,
        [
            'button[data-item-id="address"]',
            'div[data-item-id="address"]'
        ],
        attr="aria-label"
    )

    assert address != "N/A"
