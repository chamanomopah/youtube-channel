#!/usr/bin/env python3
"""
Debug script to inspect readcomiconline.li structure
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

    # Wait for page load
    time.sleep(5)

    # Try to click Server 1
    try:
        server_btns = driver.find_elements(By.XPATH, "//a[contains(text(), 'Server')]")
        if server_btns:
            print(f"Found {len(server_btns)} server buttons")
            server_btns[0].click()
            time.sleep(2)
    except Exception as e:
        print(f"Server click error: {e}")

    # Try High Quality
    try:
        quality_btns = driver.find_elements(By.XPATH, "//a[contains(text(), 'High') or contains(text(), 'Quality')]")
        if quality_btns:
            print(f"Found {len(quality_btns)} quality buttons")
            quality_btns[0].click()
            time.sleep(2)
    except Exception as e:
        print(f"Quality click error: {e}")

    # Find all images
    print("\n=== ALL IMAGES ON PAGE ===")
    all_images = driver.find_elements(By.TAG_NAME, "img")
    print(f"Total images found: {len(all_images)}\n")

    for i, img in enumerate(all_images[:30]):  # First 30 images
        try:
            src = img.get_attribute("src") or "NO SRC"
            alt = img.get_attribute("alt") or "NO ALT"
            class_attr = img.get_attribute("class") or "NO CLASS"
            id_attr = img.get_attribute("id") or "NO ID"

            size = img.size
            width = size.get('width', 0)
            height = size.get('height', 0)

            print(f"[{i}] src: {src[:100]}")
            print(f"    alt: {alt[:50]}")
            print(f"    class: {class_attr}")
            print(f"    id: {id_attr}")
            print(f"    size: {width}x{height}")
            print()
        except Exception as e:
            print(f"[{i}] Error: {e}\n")

    # Look for specific containers
    print("\n=== CHECKING SPECIFIC SELECTORS ===")
    selectors = [
        "#comicImage",
        "#mainImage",
        ".comic-page",
        ".page-image",
        "#imageContainer img",
        ".comicImg",
        "img[id*='comic']",
        "img[class*='comic']",
        "img[id*='Comic']",
        "img[class*='page']",
        "#divImage",
        "#divImage img"
    ]

    for selector in selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                print(f"✓ Found {len(elements)} elements for: {selector}")
                for el in elements[:3]:
                    src = el.get_attribute("src")
                    print(f"  src: {src[:100] if src else 'NO SRC'}")
            else:
                print(f"✗ No elements for: {selector}")
        except Exception as e:
            print(f"✗ Error with {selector}: {e}")

    # Look for blogspot images specifically
    print("\n=== BLOGSPOT IMAGES ===")
    blogspot_images = []
    for img in all_images:
        src = img.get_attribute("src") or ""
        if "blogspot" in src.lower():
            blogspot_images.append(src)

    print(f"Found {len(blogspot_images)} blogspot images:")
    for i, src in enumerate(blogspot_images[:10]):
        print(f"  [{i}] {src}")

    print("\nPress Enter to close...")
    input()

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

finally:
    driver.quit()
