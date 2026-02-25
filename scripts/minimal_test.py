#!/usr/bin/env python3
import sys
sys.path.insert(0, 'C:/Users/JOSE/Downloads/youtube-channel/scripts')

from scrape_comic_pages import find_comic_image, setup_driver
import time

url = "https://readcomiconline.li/Comic/Absolute-Batman/Issue-1?id=234426"

print("Setting up driver...")
driver = setup_driver(headless=False)

print(f"Navigating to {url}...")
driver.get(url)

print("Waiting 5 seconds...")
time.sleep(5)

print("Finding comic image...")
comic_url = find_comic_image(driver)

if comic_url:
    print(f"✓ Found comic image: {comic_url[:100]}")
else:
    print("✗ No comic image found")

print("\nClosing in 3 seconds...")
time.sleep(3)
driver.quit()
