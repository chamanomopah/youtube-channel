#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comic Page Scraper

Scrapes comic pages from readcomiconline.li with proper sequential ordering.
Usage: python selenium_webscraping_pages.py "Volume Name" <issue_number> [--url URL]
"""

import sys
import os
import re
import json
import time
import hashlib
import argparse
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
from typing import Optional

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    import requests
    from PIL import Image
except ImportError as e:
    print(f"Error: Missing required dependency: {e}")
    print("Install with: pip install selenium webdriver-manager requests pillow")
    sys.exit(1)


# Configuration
SCRIPT_DIR = Path(__file__).parent
OUTPUT_BASE_PATH = SCRIPT_DIR / "assets"
DEFAULT_COMIC_HOST = "readcomiconline.li"
REQUEST_DELAY = 1.0  # Seconds between page loads
DOWNLOAD_TIMEOUT = 15  # Seconds for image download

# HTTP Headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': f'https://{DEFAULT_COMIC_HOST}/'
}

# Comic page validation
MIN_COMIC_WIDTH = 500  # Minimum width for valid comic page
MIN_COMIC_HEIGHT = 700  # Minimum height for valid comic page
MIN_ASPECT_RATIO = 0.5  # Minimum aspect ratio (width/height)
MAX_ASPECT_RATIO = 1.5  # Maximum aspect ratio (width/height)
MIN_FILE_SIZE = 10000  # Minimum file size in bytes


def sanitize_filename(name: str) -> str:
    """
    Sanitize a string for use as a filename.

    Replaces invalid filesystem characters and limits length.
    Matches the implementation in comicvine_download_covers.py
    """
    if not name:
        return "Unnamed"

    # Replace invalid characters
    name = name.replace("/", "_")
    name = name.replace("\\", "_")
    name = name.replace(":", "_")
    name = name.replace("*", "_")
    name = name.replace("?", "_")
    name = name.replace('"', "_")
    name = name.replace("<", "_")
    name = name.replace(">", "_")
    name = name.replace("|", "_")

    # Replace spaces and multiple underscores with single underscore
    name = re.sub(r"[ _]+", "_", name)

    # Strip leading/trailing underscores and spaces
    name = name.strip("_ ")

    # Limit length to 255 characters (filesystem limit)
    if len(name) > 255:
        name = name[:255]

    return name


def get_image_hash(image_data: bytes) -> str:
    """Calculate MD5 hash of image data for duplicate detection."""
    return hashlib.md5(image_data).hexdigest()


def is_valid_comic_image(img_element, driver) -> tuple[bool, Optional[str]]:
    """
    Validate if an image element is a valid comic page.

    Returns:
        (is_valid, image_url) tuple
    """
    try:
        src = img_element.get_attribute("src")
        if not src:
            return (False, None)

        # Must be from blogspot (main comic host)
        if "blogspot.com" not in src.lower() and "bp.blogspot.com" not in src.lower():
            return (False, None)

        # Filter out known non-comic image sources
        exclude_patterns = [
            'avatar',
            'icon',
            'logo',
            'banner',
            'button',
        ]

        src_lower = src.lower()
        for pattern in exclude_patterns:
            if pattern in src_lower:
                return (False, None)

        # Check display dimensions (use what browser reports)
        size = img_element.size
        width = size.get('width', 0)
        height = size.get('height', 0)

        # Image must be large enough (use display size as proxy)
        # Blogspot comic images are typically displayed at 1000+ px width
        if width < 300:  # More permissive threshold
            return (False, None)

        return (True, src)

    except Exception as e:
        return (False, None)


def find_comic_image(driver) -> Optional[str]:
    """
    Find the main comic page image on the current page.

    Strategy: Find the largest blogspot image, which is typically the comic page.
    """
    try:
        all_images = driver.find_elements(By.TAG_NAME, "img")

        # Find all blogspot images and track the largest one
        best_image = None
        best_area = 0

        for img in all_images:
            src = img.get_attribute("src")
            if not src:
                continue

            # Must be from blogspot
            if "blogspot.com" not in src.lower() and "bp.blogspot.com" not in src.lower():
                continue

            # Get display size
            size = img.size
            width = size.get('width', 0)
            height = size.get('height', 0)

            # Must be larger than minimum
            if width < 300 or height < 300:
                continue

            # Calculate area
            area = width * height

            # Keep the largest image
            if area > best_area:
                best_area = area
                best_image = src

        return best_image

    except Exception as e:
        print(f"  [WARN] Error finding comic image: {e}")
        return None


def download_image(url: str, output_path: Path) -> bool:
    """
    Download an image from URL to output path.

    Returns:
        True if successful, False otherwise
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=DOWNLOAD_TIMEOUT)
        response.raise_for_status()

        img_data = response.content

        # Validate file size
        if len(img_data) < MIN_FILE_SIZE:
            print(f"  [WARN] Image too small ({len(img_data)} bytes)")
            return False

        # Create parent directories if needed
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Save image
        with open(output_path, "wb") as f:
            f.write(img_data)

        return True

    except requests.RequestException as e:
        print(f"  [FAIL] Download error: {e}")
        return False
    except (IOError, OSError) as e:
        print(f"  [FAIL] File save error: {e}")
        return False


def validate_downloaded_image(image_path: Path) -> bool:
    """
    Validate downloaded image using PIL.

    Checks that the image can be opened and has reasonable dimensions.
    """
    try:
        with Image.open(image_path) as img:
            width, height = img.size

            # Validate dimensions
            if width < MIN_COMIC_WIDTH or height < MIN_COMIC_HEIGHT:
                return False

            # Validate aspect ratio
            aspect_ratio = width / height
            if not (MIN_ASPECT_RATIO <= aspect_ratio <= MAX_ASPECT_RATIO):
                return False

        return True

    except Exception as e:
        print(f"  [WARN] Image validation failed: {e}")
        return False


def navigate_to_next_page(driver) -> bool:
    """
    Click the "Next" button to navigate to the next comic page.

    Returns:
        True if successful, False if no next page available
    """
    try:
        # Look for next button with multiple selectors
        next_selectors = [
            "#btnNext",
            "a[href*='next']",
            "a:contains('Next')",
            ".next-button",
            "#nextPage"
        ]

        next_btn = None
        for selector in next_selectors:
            try:
                if "contains" in selector:
                    # XPath for contains
                    next_btn = driver.find_element(By.XPATH, "//a[contains(text(), 'Next')]")
                else:
                    next_btn = driver.find_element(By.CSS_SELECTOR, selector)
                if next_btn:
                    break
            except Exception:
                continue

        if not next_btn:
            return False

        # Check if button is disabled
        class_attr = next_btn.get_attribute("class") or ""
        style_attr = next_btn.get_attribute("style") or ""

        if "disabled" in class_attr.lower():
            return False
        if "display: none" in style_attr or "display:none" in style_attr:
            return False

        # Click the button
        driver.execute_script("arguments[0].scrollIntoView();", next_btn)
        time.sleep(0.5)
        next_btn.click()

        # Wait for page to load
        time.sleep(REQUEST_DELAY)

        return True

    except Exception as e:
        print(f"  [WARN] Navigation error: {e}")
        return False


def setup_driver(headless: bool = False) -> webdriver.Chrome:
    """Set up and return Chrome WebDriver."""
    options = Options()

    if headless:
        options.add_argument("--headless")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    return driver


def sanitize_for_url(name: str) -> str:
    """
    Sanitize a string for use in readcomiconline.li URLs.

    URL format uses hyphens, not underscores.
    Example: "Absolute Batman" -> "Absolute-Batman"
    """
    if not name:
        return "Unnamed"

    # Replace invalid characters
    name = name.replace("/", "-")
    name = name.replace("\\", "-")
    name = name.replace(":", "-")
    name = name.replace("*", "-")
    name = name.replace("?", "-")
    name = name.replace('"', "-")
    name = name.replace("<", "-")
    name = name.replace(">", "-")
    name = name.replace("|", "-")
    name = name.replace("_", "-")  # Also replace underscores with hyphens

    # Replace spaces and multiple hyphens with single hyphen
    name = re.sub(r"[ -]+", "-", name)

    # Strip leading/trailing hyphens and spaces
    name = name.strip("- ")

    # Limit length
    if len(name) > 255:
        name = name[:255]

    return name


def construct_comic_url(volume_name: str, issue_number: str) -> str:
    """
    Construct readcomiconline.li URL from volume name and issue number.

    Example: "Absolute Batman" + "1" -> https://readcomiconline.li/Comic/Absolute-Batman/Issue-1
    """
    sanitized_volume = sanitize_for_url(volume_name)
    url = f"https://{DEFAULT_COMIC_HOST}/Comic/{sanitized_volume}/Issue-{issue_number}"
    return url


def scrape_issue(volume_name: str, issue_number: str, url: Optional[str] = None, headless: bool = False):
    """
    Scrape all pages from a comic issue.

    Args:
        volume_name: Name of the comic volume
        issue_number: Issue number
        url: Optional URL override (auto-constructed if not provided)
        headless: Run browser in headless mode
    """
    # Construct URL if not provided
    if not url:
        url = construct_comic_url(volume_name, issue_number)

    print(f"Scraping: {volume_name} #{issue_number}")
    print(f"URL: {url}")
    print()

    # Set up output directory
    sanitized_volume = sanitize_filename(volume_name)
    output_dir = OUTPUT_BASE_PATH / sanitized_volume / "issues" / issue_number / "pages"

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Check for existing pages (resume capability)
    existing_pages = sorted(output_dir.glob("page_*.jpg"))
    if existing_pages:
        print(f"[INFO] Found {len(existing_pages)} existing pages")
        print(f"[INFO] Resuming from page {len(existing_pages) + 1}...")

    # Set up Selenium driver
    driver = setup_driver(headless=headless)

    try:
        # Navigate to URL
        driver.get(url)

        # Wait for initial page load
        time.sleep(5)

        # Try to click Server 1 if available
        try:
            server_btns = driver.find_elements(By.XPATH, "//a[contains(text(), 'Server')]")
            if server_btns:
                server_btns[0].click()
                time.sleep(1)
        except Exception:
            pass

        # Try to click High Quality if available
        try:
            quality_btns = driver.find_elements(By.XPATH, "//a[contains(text(), 'High') or contains(text(), 'Quality')]")
            if quality_btns:
                quality_btns[0].click()
                time.sleep(2)
        except Exception:
            pass

        # Scrape pages
        page_num = len(existing_pages) + 1
        max_pages = 200  # Safety limit
        downloaded_pages = []
        previous_hash = None

        print("Starting scrape...")
        print("=" * 50)

        while page_num <= max_pages:
            # Wait for image to load on each page
            time.sleep(3)

            # Find comic image
            comic_url = find_comic_image(driver)

            if not comic_url:
                print(f"[{page_num}] [FAIL] No comic image found")
                break

            # Download page
            ext = ".jpg"
            if ".png" in comic_url:
                ext = ".png"
            elif ".webp" in comic_url:
                ext = ".webp"

            filename = f"page_{page_num:03d}{ext}"
            output_path = output_dir / filename

            # Check if file already exists
            if output_path.exists():
                print(f"[{page_num}] [SKIP] Already downloaded")

                # Read hash for duplicate detection
                with open(output_path, "rb") as f:
                    previous_hash = get_image_hash(f.read())

                # Navigate to next page
                if not navigate_to_next_page(driver):
                    break

                page_num += 1
                continue

            # Download image
            print(f"[{page_num}] Downloading: {comic_url[:70]}...")

            if download_image(comic_url, output_path):
                # Validate downloaded image
                if validate_downloaded_image(output_path):
                    print(f"[{page_num}] [OK] Downloaded")

                    # Check for duplicates
                    with open(output_path, "rb") as f:
                        current_hash = get_image_hash(f.read())

                    if previous_hash and current_hash == previous_hash:
                        print(f"[{page_num}] [WARN] Duplicate detected (end of comic)")
                        output_path.unlink()  # Remove duplicate
                        break

                    previous_hash = current_hash
                    downloaded_pages.append({
                        "page_number": page_num,
                        "filename": filename,
                        "url": comic_url,
                        "hash": current_hash
                    })

                else:
                    print(f"[{page_num}] [FAIL] Image validation failed")
                    output_path.unlink()  # Remove invalid image
                    break
            else:
                print(f"[{page_num}] [FAIL] Download failed")
                break

            # Navigate to next page
            if not navigate_to_next_page(driver):
                print(f"\n[INFO] No more pages")
                break

            page_num += 1

        # Save metadata
        metadata = {
            "volume": volume_name,
            "issue": issue_number,
            "url": url,
            "total_pages": page_num - 1,
            "pages": downloaded_pages,
            "scraped_at": datetime.now().isoformat(),
            "output_directory": str(output_dir)
        }

        metadata_path = output_dir.parent / "metadata.json"
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        # Print summary
        print("\n" + "=" * 50)
        print("Scrape Summary")
        print("=" * 50)
        print(f"Volume: {volume_name}")
        print(f"Issue: {issue_number}")
        print(f"Total pages: {page_num - 1}")
        print(f"Output directory: {output_dir.absolute()}")
        print(f"Metadata saved: {metadata_path.absolute()}")
        print("=" * 50)

    except KeyboardInterrupt:
        print("\n\nScraping cancelled by user.")

    finally:
        driver.quit()


def main():
    """Main execution flow."""
    parser = argparse.ArgumentParser(
        description="Scrape comic pages from readcomiconline.li",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape Absolute Batman #1 (auto-constructs URL)
  python selenium_webscraping_pages.py "Absolute Batman" 1

  # Scrape with specific URL
  python selenium_webscraping_pages.py "Absolute Batman" 1 --url "https://readcomiconline.li/Comic/Absolute-Batman/Issue-1?id=234426"

  # Run in headless mode
  python selenium_webscraping_pages.py "Absolute Batman" 1 --headless

Output Structure:
  scripts/assets/<Volume_Name>/issues/<Issue_Number>/pages/page_001.jpg
  scripts/assets/<Volume_Name>/issues/<Issue_Number>/metadata.json
        """
    )

    parser.add_argument(
        "volume",
        help="Comic volume name (e.g., 'Absolute Batman')"
    )

    parser.add_argument(
        "issue",
        help="Issue number (e.g., '1', '2', 'Annual 1')"
    )

    parser.add_argument(
        "--url",
        help="Override auto-constructed URL",
        default=None
    )

    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode (no GUI)"
    )

    args = parser.parse_args()

    # Scrape the issue
    scrape_issue(args.volume, args.issue, args.url, args.headless)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScraping cancelled by user.")
        sys.exit(0)
