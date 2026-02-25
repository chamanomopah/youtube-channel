# Bug: Comic Scraper Downloads Multiple Issues Instead of Single Specified Issue

## Bug Description
The comic scraper script (`selenium_webscraping_pages.py`) downloads pages from multiple issues when only a single issue is specified. When the "Next" button is clicked from the last page of an issue, the website navigates to the first page of the next issue, but the script continues downloading without detecting this transition.

## Problem Statement
When running `python scripts\selenium_webscraping_pages.py "Absolute Batman" 1`, the script should only download pages from Issue #1. However, it continues through Issues #2, #3, #4, etc., because:

1. **No Issue Boundary Detection**: The script doesn't detect when it has crossed from one issue to another
2. **No Page Count Validation**: The script doesn't check the page count indicator on the website
3. **Always Requires Issue Number**: The current implementation requires an issue number argument, preventing the "download all issues" use case

## Solution Statement
The script should:

1. **For specific issue**: When an issue number is provided (e.g., `python script "Absolute Batman" 7`), download ONLY that issue and stop when reaching the page limit or next issue
2. **For all issues**: When NO issue number is provided (e.g., `python script "Absolute Batman"`), download ALL issues in the volume
3. **Detect issue transitions**: Monitor URL changes and page indicators to detect when moving to a new issue
4. **Organize by issue**: When crossing to next issue, save pages to the correct issue folder

## Steps to Reproduce
1. Run `python scripts\selenium_webscraping_pages.py "Absolute Batman" 1`
2. Wait for the script to download pages from Issue #1
3. After the last page of Issue #1, the script clicks "Next"
4. The website loads Issue #2, Page 1
5. The script continues downloading, saving Issue #2 pages as Issue #1 pages
6. User must cancel with Ctrl+C after noticing 131+ pages downloaded

**Expected**: Script downloads only the ~30-40 pages from Issue #1, then stops
**Actual**: Script downloads 131+ pages across 4+ issues without stopping

## Root Cause Analysis

### Primary Cause: Absence of Issue Boundary Detection

The `navigate_to_next_page()` function (line 251-305) simply clicks the Next button and returns `True` without verifying:
1. Whether the URL has changed to a different issue
2. Whether the page number indicator has reset
3. Whether we've exceeded the expected page count for this issue

### Secondary Cause: Inflexible CLI Design

The `main()` function (line 551-598) requires both `volume` AND `issue` arguments:
```python
parser.add_argument("volume", help="Comic volume name")
parser.add_argument("issue", help="Issue number")
```

This prevents the user from requesting "all issues" without manually running the script multiple times.

### Website Behavior (from readcomiconline.li)

Based on the user's description:
- URL pattern: `https://readcomiconline.li/Comic/<Volume>/Issue-<Number>`
- Each page has a page indicator (e.g., "Page 5/32")
- Clicking "Next" from the last page of Issue N goes to Issue N+1, Page 1
- The issue number is embedded in the URL path

### Current Code Flow

```
scrape_issue(volume, issue_number)
  ├── Loop: page_num = 1 to max_pages (200)
  │   ├── Find comic image
  │   ├── Download to: output_dir/page_<num>.jpg
  │   ├── navigate_to_next_page()
  │   │   └── Click Next button (NO ISSUE CHECK!)
  │   └── page_num += 1
  └── Never checks if issue changed!
```

### Why 131 Pages Were Downloaded

- Issue #1: ~33 pages
- Issue #2: ~33 pages
- Issue #3: ~33 pages
- Issue #4: ~32 pages
- Total: ~131 pages

The script continued until `max_pages=200` or user cancellation.

## Relevant Files

### Primary Files
- `scripts/selenium_webscraping_pages.py` (lines 251-305: `navigate_to_next_page`)
- `scripts/selenium_webscraping_pages.py` (lines 374-548: `scrape_issue`)
- `scripts/selenium_webscraping_pages.py` (lines 551-598: `main`)
- `scripts/selenium_webscraping_pages.py` (lines 363-371: `construct_comic_url`)

### Reference Files
- `scripts/README_COMIC_SCRAPER.md` (documentation)
- `scripts/assets/` (output directory structure)

## Step by Step Tasks

### Task 1: Extract Issue Number from URL
**File**: `scripts/selenium_webscraping_pages.py`
**Location**: Add new function after `construct_comic_url` (around line 372)

```python
def extract_issue_number_from_url(url: str) -> Optional[str]:
    """
    Extract issue number from readcomiconline.li URL.

    Example: "https://readcomiconline.li/Comic/Absolute-Batman/Issue-1"
             -> "1"
    """
    import re
    match = re.search(r'/Issue-([^/]+)', url)
    if match:
        return match.group(1)
    return None
```

### Task 2: Extract Page Count Indicator
**File**: `scripts/selenium_webscraping_pages.py`
**Location**: Add new function after Task 1

```python
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
```

### Task 3: Modify navigate_to_next_page to Detect Issue Changes
**File**: `scripts/selenium_webscraping_pages.py`
**Location**: Modify `navigate_to_next_page` function (lines 251-305)

Changes:
1. Capture URL before clicking
2. After clicking, check if URL issue number changed
3. Return tuple: `(success, current_issue_number)`

```python
def navigate_to_next_page(driver) -> tuple[bool, Optional[str]]:
    """
    Click the "Next" button and detect if we've moved to a new issue.

    Returns:
        (success, issue_number) tuple where:
        - success: True if navigation succeeded
        - issue_number: Current issue number after navigation, or None
    """
    # Get current URL before navigation
    current_url = driver.current_url
    current_issue = extract_issue_number_from_url(current_url)

    try:
        # ... existing next button finding code ...

        if not next_btn:
            return (False, current_issue)

        # ... existing button click code ...

        # Click the button
        next_btn.click()
        time.sleep(REQUEST_DELAY)

        # Get new URL after navigation
        new_url = driver.current_url
        new_issue = extract_issue_number_from_url(new_url)

        return (True, new_issue)

    except Exception as e:
        return (False, current_issue)
```

### Task 4: Add Function to Scrape All Issues
**File**: `scripts/selenium_webscraping_pages.py`
**Location**: Add new function after `scrape_issue`

```python
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

            # Scrape this issue
            scrape_issue(volume_name, issue_number_str, url, headless)
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
```

### Task 5: Modify scrape_issue to Stop at Issue Boundary
**File**: `scripts/selenium_webscraping_pages.py`
**Location**: Modify the main loop in `scrape_issue` (lines 442-516)

Changes:
1. Add `expected_issue` parameter
2. Check page count indicator
3. Detect issue changes during navigation
4. Stop when issue changes or page count reached

```python
def scrape_issue(volume_name: str, issue_number: str, url: Optional[str] = None,
                 headless: bool = False, stop_at_next_issue: bool = True):
    """
    Scrape all pages from a comic issue.

    Args:
        volume_name: Name of the comic volume
        issue_number: Issue number
        url: Optional URL override
        headless: Run browser in headless mode
        stop_at_next_issue: Stop when reaching next issue (default: True)
    """
    # ... existing setup code ...

    expected_issue = issue_number
    total_pages_expected = None
    pages_downloaded = 0

    # ... existing driver setup and URL navigation ...

    # Get initial page count
    current_page, total_pages = get_page_count_indicator(driver)
    if total_pages:
        total_pages_expected = total_pages
        print(f"[INFO] Page count indicator: {total_pages} pages")

    # Main scrape loop
    while page_num <= max_pages:
        # ... existing image download code ...

        # Check page count against indicator
        if total_pages_expected and page_num > total_pages_expected:
            print(f"\n[INFO] Reached expected page count ({total_pages_expected})")
            break

        # Navigate to next page
        success, current_issue = navigate_to_next_page(driver)

        if not success:
            print(f"\n[INFO] No more pages")
            break

        # Check if we've moved to a new issue
        if stop_at_next_issue and current_issue != expected_issue:
            print(f"\n[INFO] Reached next issue (Issue #{current_issue})")
            print(f"[INFO] Stopping at issue boundary")
            break

        page_num += 1
```

### Task 6: Update CLI Arguments for Optional Issue Number
**File**: `scripts/selenium_webscraping_pages.py`
**Location**: Modify `main` function (lines 551-598)

Changes:
1. Make `issue` argument optional
2. Add logic to detect whether to scrape single issue or all issues

```python
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
        help="Issue number (e.g., '1', '2'). If not specified, scrapes ALL issues"
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

    # Route to appropriate function
    if args.issue is None:
        # Scrape all issues
        scrape_all_issues(args.volume, start_issue=1, headless=args.headless)
    else:
        # Scrape single issue
        scrape_issue(args.volume, args.issue, args.url, args.headless, stop_at_next_issue=True)
```

### Task 7: Update Documentation
**File**: `scripts/README_COMIC_SCRAPER.md`

Add new usage examples:

```markdown
### Scraping Modes

#### Single Issue Mode
Scrape only the specified issue:

```bash
python scripts/selenium_webscraping_pages.py "Absolute Batman" 7
```

#### All Issues Mode
Scrape all issues in a volume:

```bash
python scripts/selenium_webscraping_pages.py "Absolute Batman"
```

The script will automatically detect when to stop (404 or no images found).
```

### Task 8: Add URL Change Detection Helper
**File**: `scripts/selenium_webscraping_pages.py`
**Location**: Add after `extract_issue_number_from_url`

```python
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
```

## Validation Commands

### Test 1: Verify Single Issue Stops at Boundary
```bash
# Test: Should download ONLY Issue #1 (approx 30-40 pages), then stop
python scripts/selenium_webscraping_pages.py "Absolute Batman" 1

# Verify: Check that only Issue #1 folder exists and has reasonable page count
ls scripts/assets/Absolute_Batman/issues/1/pages/
# Expected: ~30-40 files named page_001.jpg through page_0XX.jpg
# Expected: NO Issue #2, #3, #4 folders created

# Verify page count is reasonable
ls scripts/assets/Absolute_Batman/issues/1/pages/ | wc -l
# Expected: 30-50 (not 131!)
```

### Test 2: Verify All Issues Mode
```bash
# Test: Should download ALL issues until 404
python scripts/selenium_webscraping_pages.py "Absolute Batman" --headless

# Verify: Multiple issue folders created
ls scripts/assets/Absolute_Batman/issues/
# Expected: 1/, 2/, 3/, 4/, etc. (all available issues)

# Verify each issue has its own pages
for i in 1 2 3 4 5; do
    echo "Issue #$i:"
    ls scripts/assets/Absolute_Batman/issues/$i/pages/ | wc -l
done
```

### Test 3: Verify Issue Number Extraction
```bash
python -c "
from selenium_webscraping_pages import extract_issue_number_from_url

# Test cases
assert extract_issue_number_from_url('https://readcomiconline.li/Comic/Absolute-Batman/Issue-1') == '1'
assert extract_issue_number_from_url('https://readcomiconline.li/Comic/Absolute-Batman/Issue-7?id=12345') == '7'
assert extract_issue_number_from_url('https://readcomiconline.li/Comic/Absolute-Batman') is None

print('✓ Issue number extraction tests passed')
"
```

### Test 4: Verify URL Construction
```bash
python -c "
from selenium_webscraping_pages import construct_comic_url

url = construct_comic_url('Absolute Batman', '7')
expected = 'https://readcomiconline.li/Comic/Absolute-Batman/Issue-7'
assert url == expected, f'Expected {expected}, got {url}'

print('✓ URL construction test passed')
"
```

### Test 5: Integration Test
```bash
# Full workflow test
rm -rf scripts/assets/Test_Comic
python scripts/selenium_webscraping_pages.py "Absolute Batman" 1

# Verify metadata contains correct issue number
cat scripts/assets/Absolute_Batman/issues/1/metadata.json | grep '"issue"'
# Expected: "issue": "1"

# Verify no cross-contamination
if [ -d "scripts/assets/Absolute_Batman/issues/2" ]; then
    echo "FAIL: Issue #2 folder should not exist!"
    exit 1
fi

echo "✓ Integration test passed"
```

### Test 6: Reproduce Original Bug (Should Now Fail)
```bash
# This should now STOP after Issue #1, not continue to #2, #3, #4
python scripts/selenium_webscraping_pages.py "Absolute Batman" 1

# After completion, verify no cross-issue contamination
find scripts/assets/Absolute_Batman/issues/ -name "page_*" | wc -l
# Expected: Should match issue #1's page count (30-50)
# NOT 131+ (the bug result)
```

## Notes

### Regression Risks
1. **Existing Scraped Data**: Users who have run the script before may have mixed issues in folders. Consider adding a migration script.
2. **URL Pattern Changes**: If readcomiconline.li changes URL structure, `extract_issue_number_from_url` will break.
3. **Page Indicator Reliability**: The page count indicator may not be present on all issues.

### Edge Cases to Monitor
1. **Special Issues**: "Annual 1", "Special #1", etc. may have different URL patterns
2. **One-Shots**: Issues with only one page or very short issues
3. **Missing Issues**: Gaps in issue numbering (e.g., Volume has #1, #2, #4 but no #3)
4. **Network Issues**: Timeout or 503 errors during navigation

### Future Enhancements
1. **Resume All Issues**: Allow resuming interrupted "all issues" downloads
2. **Issue Range**: Support ranges like `python script "Batman" 1-10`
3. **Progress Bar**: Show progress across all issues in "all issues" mode
4. **Parallel Scraping**: Scrape multiple issues concurrently (with rate limiting)

### Related Issues
- None currently documented, but the `comicvine_download_covers.py` script may have similar issues if it iterates through issues

### Monitoring Points
After deployment, monitor:
1. User reports of "script stopped too early" (may indicate page count detection issues)
2. User reports of "still downloading wrong issues" (indicates boundary detection failure)
3. Error logs for URL parsing failures
