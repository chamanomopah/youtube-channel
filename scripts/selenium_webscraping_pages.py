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
            aspect_ratio = width / height

            # Validate dimensions with detailed logging
            if width < MIN_COMIC_WIDTH:
                print(f"  [VALIDATE] FAIL: width {width} < MIN_COMIC_WIDTH {MIN_COMIC_WIDTH}")
                return False
            if height < MIN_COMIC_HEIGHT:
                print(f"  [VALIDATE] FAIL: height {height} < MIN_COMIC_HEIGHT {MIN_COMIC_HEIGHT}")
                return False

            # Validate aspect ratio with detailed logging
            if aspect_ratio < MIN_ASPECT_RATIO:
                print(f"  [VALIDATE] FAIL: aspect {aspect_ratio:.2f} < MIN_ASPECT_RATIO {MIN_ASPECT_RATIO}")
                return False
            if aspect_ratio > MAX_ASPECT_RATIO:
                print(f"  [VALIDATE] FAIL: aspect {aspect_ratio:.2f} > MAX_ASPECT_RATIO {MAX_ASPECT_RATIO}")
                return False

        return True

    except Exception as e:
        print(f"  [WARN] Image validation failed: {e}")
        return False


def navigate_to_next_page(driver) -> tuple[bool, Optional[str], Optional[int], Optional[str]]:
    """
    Click the "Next" button and detect if we've moved to a new issue.

    Returns:
        (success, issue_number, page_fragment, page_title) tuple where:
        - success: True if navigation succeeded
        - issue_number: Current issue number after navigation, or None
        - page_fragment: Page number from URL fragment (e.g., #13 -> 13), or None
        - page_title: Page title (may contain issue info), or None
    """
    # Get current URL before navigation
    current_url = driver.current_url
    current_issue = extract_issue_number_from_url(current_url)

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
            return (False, current_issue, None, None)

        # Check if button is disabled
        class_attr = next_btn.get_attribute("class") or ""
        style_attr = next_btn.get_attribute("style") or ""

        if "disabled" in class_attr.lower():
            return (False, current_issue, None, None)
        if "display: none" in style_attr or "display:none" in style_attr:
            return (False, current_issue, None, None)

        # Click the button
        driver.execute_script("arguments[0].scrollIntoView();", next_btn)
        time.sleep(0.5)
        next_btn.click()

        # Wait for page to load
        time.sleep(REQUEST_DELAY)

        # Get new URL after navigation
        new_url = driver.current_url
        new_issue = extract_issue_number_from_url(new_url)

        # Extract page number from URL fragment (#13 -> 13)
        page_fragment = None
        fragment_match = re.search(r'#(\d+)', new_url)
        if fragment_match:
            page_fragment = int(fragment_match.group(1))

        # Get page title for issue detection
        page_title = None
        try:
            page_title = driver.title
        except Exception:
            pass

        # DEBUG: Log URL changes
        if current_url != new_url:
            print(f"  [DEBUG] URL: {new_url[:80]}...")
            print(f"  [DEBUG] Title: {page_title[:60] if page_title else 'N/A'}...")

        return (True, new_issue, page_fragment, page_title)

    except Exception as e:
        print(f"  [WARN] Navigation error: {e}")
        return (False, current_issue, None, None)


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


def extract_issue_number_from_url(url: str) -> Optional[str]:
    """
    Extract issue number from readcomiconline.li URL.

    Example: "https://readcomiconline.li/Comic/Absolute-Batman/Issue-1"
             -> "1"
    Example: "https://readcomiconline.li/Comic/Absolute-Batman/Issue-1#2"
             -> "1" (page fragments are ignored)
    """
    match = re.search(r'/Issue-([^/?#]+)', url)
    if match:
        return match.group(1)
    return None


def get_page_count_indicator(driver) -> tuple[Optional[int], Optional[int]]:
    """
    Extract current page and total pages from website indicator.

    Returns:
        (current_page, total_pages) tuple or (None, None) if not found
    """
    try:
        # Look for page indicator elements (various formats)
        selectors = [
            "//span[contains(text(), 'Page')]",
            "//div[contains(text(), '/')]",
            "//*[@class='pageIndicator']",
            "//*[@id='pageIndicator']"
        ]

        for selector in selectors:
            try:
                element = driver.find_element(By.XPATH, selector)
                text = element.text.strip()

                # Parse "Page 5/32" or "5/32" formats
                match = re.search(r'(\d+)\s*/\s*(\d+)', text)
                if match:
                    current = int(match.group(1))
                    total = int(match.group(2))
                    return (current, total)
            except Exception:
                continue

        return (None, None)
    except Exception:
        return (None, None)


def has_issue_changed(driver: webdriver.Chrome, expected_issue: str) -> bool:
    """
    Check if the current page is from a different issue than expected.

    Args:
        driver: Selenium WebDriver instance
        expected_issue: The issue number we expect to be on

    Returns:
        True if issue has changed, False otherwise
    """
    current_url = driver.current_url
    current_issue = extract_issue_number_from_url(current_url)

    if current_issue is None:
        return False

    return current_issue != expected_issue


def scrape_issue(volume_name: str, issue_number: str, url: Optional[str] = None,
                 headless: bool = False, stop_at_next_issue: bool = True):
    """
    Scrape all pages from a comic issue.

    Args:
        volume_name: Name of the comic volume
        issue_number: Issue number
        url: Optional URL override (auto-constructed if not provided)
        headless: Run browser in headless mode
        stop_at_next_issue: Stop when reaching next issue (default: True)
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
        # Extract page numbers from filenames to find the actual last page
        page_numbers = []
        for p in existing_pages:
            match = re.search(r'page_(\d+)', p.name)
            if match:
                page_numbers.append(int(match.group(1)))

        if page_numbers:
            last_page = max(page_numbers)
            print(f"[INFO] Found {len(existing_pages)} existing pages")
            print(f"[INFO] Last page found: {last_page}")
            print(f"[INFO] Resuming from page {last_page + 1}...")
            start_page = last_page + 1
        else:
            start_page = 1
    else:
        start_page = 1

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
        page_num = start_page
        max_pages = 40  # Safety limit - most issues have < 40 pages
        downloaded_pages = []
        previous_hash = None
        all_hashes = set()  # Track ALL hashes to detect duplicates across pages

        print(f"[INFO] Starting from page {page_num} (max: {max_pages})")
        print("[INFO] Will stop if detecting next issue or reaching page limit")
        print()

        # Issue boundary detection
        expected_issue = issue_number
        total_pages_expected = None

        # Get initial page count indicator
        current_page, total_pages = get_page_count_indicator(driver)
        if total_pages:
            total_pages_expected = total_pages
            print(f"[INFO] Page count indicator: {total_pages} pages")

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
                    file_hash = get_image_hash(f.read())
                    previous_hash = file_hash
                    all_hashes.add(file_hash)

                # Check page count against indicator
                if total_pages_expected and page_num > total_pages_expected:
                    print(f"\n[INFO] Reached expected page count ({total_pages_expected})")
                    break

                # Navigate to next page
                success, current_issue, page_fragment, page_title = navigate_to_next_page(driver)

                if not success:
                    print(f"\n[INFO] No more pages")
                    break

                # Check if we've moved to a new issue
                if stop_at_next_issue and current_issue is not None and current_issue != expected_issue:
                    print(f"\n[INFO] Reached next issue (Issue #{current_issue})")
                    print(f"[INFO] Stopping at issue boundary")
                    break

                page_num += 1
                continue

            # Download image
            print(f"[{page_num}] Downloading: {comic_url[:70]}...")

            if download_image(comic_url, output_path):
                # Validate downloaded image
                if validate_downloaded_image(output_path):
                    print(f"[{page_num}] [OK] Downloaded")

                    # Check for duplicates against ALL downloaded pages
                    with open(output_path, "rb") as f:
                        current_hash = get_image_hash(f.read())

                    if current_hash in all_hashes:
                        print(f"[{page_num}] [WARN] Duplicate detected (image already downloaded)")
                        print(f"[{page_num}] [WARN] This is likely the next issue - stopping")
                        output_path.unlink()  # Remove duplicate
                        break

                    previous_hash = current_hash
                    all_hashes.add(current_hash)
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

            # Check page count against indicator
            if total_pages_expected and page_num > total_pages_expected:
                print(f"\n[INFO] Reached expected page count ({total_pages_expected})")
                break

            # Navigate to next page
            success, current_issue, page_fragment, page_title = navigate_to_next_page(driver)

            if not success:
                print(f"\n[INFO] No more pages")
                break

            # Check if we've moved to a new issue
            if stop_at_next_issue and current_issue is not None and current_issue != expected_issue:
                print(f"\n[INFO] Reached next issue (Issue #{current_issue})")
                print(f"[INFO] Stopping at issue boundary")
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


def scrape_all_issues(volume_name: str, start_issue: int = 1, headless: bool = False):
    """
    Scrape all issues from a comic volume starting from the specified issue.

    Args:
        volume_name: Name of the comic volume
        start_issue: First issue to scrape (default: 1)
        headless: Run browser in headless mode
    """
    current_issue_num = start_issue
    total_issues = 0

    print(f"Scraping all issues of {volume_name} (starting from #{current_issue_num})")
    print("=" * 50)

    while current_issue_num <= 100:  # Safety limit
        # Construct URL for this issue
        url = construct_comic_url(volume_name, str(current_issue_num))
        issue_number_str = str(current_issue_num)

        print(f"\nAttempting Issue #{current_issue_num}...")
        print(f"URL: {url}")

        # Set up driver to check if issue exists
        driver = setup_driver(headless=headless)

        try:
            driver.get(url)
            time.sleep(5)

            # Check if we got a 404 or "Issue not found" page
            page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
            if "not found" in page_text or "404" in page_text:
                print(f"[INFO] Issue #{current_issue_num} does not exist. Stopping.")
                break

            # Check if comic image exists
            if not find_comic_image(driver):
                print(f"[INFO] No comic images found for Issue #{current_issue_num}. Stopping.")
                break

            driver.quit()

            # Scrape this issue (with stop_at_next_issue=True to be safe)
            scrape_issue(volume_name, issue_number_str, url, headless, stop_at_next_issue=True)
            total_issues += 1
            current_issue_num += 1

        except Exception as e:
            print(f"[ERROR] Error checking issue #{current_issue_num}: {e}")
            driver.quit()
            break

    print("\n" + "=" * 50)
    print(f"All issues scraping complete!")
    print(f"Total issues scraped: {total_issues}")
    print("=" * 50)


def main():
    """Main execution flow."""
    parser = argparse.ArgumentParser(
        description="Scrape comic pages from readcomiconline.li",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape ALL issues of Absolute Batman
  python selenium_webscraping_pages.py "Absolute Batman"

  # Scrape only Absolute Batman #7
  python selenium_webscraping_pages.py "Absolute Batman" 7

  # Scrape with specific URL
  python selenium_webscraping_pages.py "Absolute Batman" 1 --url "https://..."

  # Run in headless mode
  python selenium_webscraping_pages.py "Absolute Batman" --headless

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
        nargs='?',  # Optional argument
        default=None,
        help="Issue number (e.g., '1', '2', 'Annual 1'). If not specified, scrapes ALL issues"
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

    # Route to appropriate function based on whether issue number is provided
    if args.issue is None:
        # Scrape all issues
        scrape_all_issues(args.volume, start_issue=1, headless=args.headless)
    else:
        # Scrape single issue
        scrape_issue(args.volume, args.issue, args.url, args.headless, stop_at_next_issue=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScraping cancelled by user.")
        sys.exit(0)
