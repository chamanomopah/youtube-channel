#!/usr/bin/env python3
import sys
sys.path.insert(0, 'C:/Users/JOSE/Downloads/youtube-channel/scripts')

from scrape_comic_pages import scrape_issue

# Test with explicit URL
url = "https://readcomiconline.li/Comic/Absolute-Batman/Issue-1?id=234426"
print("Testing scrape_issue with URL:", url)
print()

try:
    scrape_issue("Absolute Batman", "1", url=url, headless=False)
    print("\nTest completed")
except Exception as e:
    print(f"\nTest failed with error: {e}")
    import traceback
    traceback.print_exc()
