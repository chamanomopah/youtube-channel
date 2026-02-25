#!/usr/bin/env python3
"""
Quick test of the scraper with debug output
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

url = "https://readcomiconline.li/Comic/Absolute-Batman/Issue-1?id=234426"

options = Options()
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    print("Loading page...")
    driver.get(url)
    time.sleep(5)

    print("\nLooking for Server buttons...")
    server_btns = driver.find_elements(By.XPATH, "//a[contains(text(), 'Server')]")
    print(f"Found {len(server_btns)} Server buttons")
    if server_btns:
        print("Clicking first Server button...")
        server_btns[0].click()
        time.sleep(2)

    print("\nLooking for Quality buttons...")
    quality_btns = driver.find_elements(By.XPATH, "//a[contains(text(), 'High') or contains(text(), 'Quality')]")
    print(f"Found {len(quality_btns)} Quality buttons")
    if quality_btns:
        print("Clicking first Quality button...")
        quality_btns[0].click()
        time.sleep(3)

    print("\nLooking for blogspot images...")
    all_images = driver.find_elements(By.TAG_NAME, "img")
    print(f"Total images: {len(all_images)}")

    blogspot_images = []
    for img in all_images:
        src = img.get_attribute("src") or ""
        if "blogspot" in src.lower():
            size = img.size
            width = size.get('width', 0)
            height = size.get('height', 0)
            area = width * height
            blogspot_images.append((area, width, height, src))
            print(f"  Blogspot image: {width}x{height} (area={area})")
            print(f"    URL: {src[:80]}...")

    print(f"\nTotal blogspot images: {len(blogspot_images)}")

    if blogspot_images:
        blogspot_images.sort(reverse=True)
        best = blogspot_images[0]
        print(f"\nLargest image: {best[1]}x{best[2]} (area={best[0]})")
        print(f"URL: {best[3]}")
    else:
        print("\nNo blogspot images found!")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

finally:
    print("\nPress Enter to close...")
    input()
    driver.quit()
