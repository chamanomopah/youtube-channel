# Feature: Improved Comic Page Scraper with Proper Ordering

## Feature Description
Enhance the Selenium-based comic page scraper to precisely target comic page images (not UI elements or ads) and ensure strict sequential page ordering from first to last. The scraper will follow the existing project conventions established by `comicvine_download_covers.py`.

## User Story
As a video producer creating "Every Comic Explained" videos, I want to scrape comic pages in correct sequential order without capturing non-comic images, so that my Remotion video pipeline can display pages in the proper reading order.

## Problem Statement
The current `selenium_webscraping_pages.py` script has three critical issues:

1. **Incorrect image targeting**: Scrapes ALL blogspot images >300px, including UI elements, ads, and non-comic content
2. **Hardcoded URL**: Only works for Absolute Batman #1, requiring code edits to change comics
3. **Poor organization**: Saves files flat to `pages/` without volume/issue structure or metadata

## Solution Statement
Refactor the scraper to:
- Target only the actual comic page image container using specific CSS selectors
- Accept command-line arguments for volume name and issue number
- Organize output in `scripts/assets/<Volume>/issues/<Issue>/pages/` structure
- Save metadata JSON for Remotion integration
- Follow project conventions from `comicvine_download_covers.py`

## Relevant Files

### New Files
- `scripts/scrape_comic_pages.py` (Enhanced scraper with proper structure)

### Modified Files
- `scripts/selenium_webscraping_pages.py` (May be replaced or deprecated)

## Implementation Plan

### Foundation Phase
1. **Analyze readcomiconline.li DOM structure**: Identify exact CSS selectors for comic page images vs navigation/ads
2. **Design directory structure**: Define output path format matching project conventions
3. **Add command-line argument parsing**: Use argparse for volume name, issue number, optional URL
4. **Create utility functions**: Port `sanitize_filename()`, status indicators from cover downloader

### Core Phase
1. **Implement precise image targeting**:
   - Find the main comic image container (typically a specific div or img class)
   - Verify aspect ratio matches comic pages (~0.66 for standard US comics)
   - Filter out non-comic images using URL patterns and dimensions

2. **Implement strict sequential navigation**:
   - Locate and click the "Next" button using reliable selectors
   - Wait for page load with explicit waits
   - Track page numbers incrementally
   - Handle edge cases: disabled buttons, redirects, duplicate last pages

3. **Add metadata tracking**:
   - Save issue metadata (URL, page count, timestamp) to JSON
   - Store in `scripts/assets/<Volume>/issues/<Issue>/metadata.json`

### Integration Phase
1. **Match project conventions**: Use same status indicators, error handling, progress format
2. **Add resume capability**: Check existing directory, skip downloaded pages
3. **Create usage documentation**: Document arguments, output structure, examples

## Step by Step Tasks
1. Inspect readcomiconline.li HTML to identify comic image container CSS selector
2. Create `scripts/scrape_comic_pages.py` with argparse setup for volume/issue arguments
3. Implement `find_comic_image()` function using precise CSS selectors
4. Implement `download_page()` with validation (aspect ratio, size checks)
5. Implement `navigate_next()` with proper waits and button detection
6. Add main loop with sequential page tracking (page_001, page_002, etc.)
7. Create directory structure: `assets/<sanitized_volume>/issues/<issue>/pages/`
8. Save metadata.json with issue info and page manifest
9. Add duplicate detection using byte comparison or hash
10. Add resume capability: skip existing pages in directory
11. Add progress indicators matching cover downloader style
12. Test with Absolute Batman #1 (known working URL)
13. Test with different comic to verify CSS selectors work generally

## Testing Strategy

### Unit Tests
- Test `sanitize_filename()` with various comic titles (special chars, spaces)
- Test `find_comic_image()` with mock DOM containing comic vs non-comic images
- Test `is_valid_comic_page()` with various aspect ratios and dimensions
- Test path construction for various volume/issue combinations

### Integration Tests
- Scrape Absolute Batman #1 completely and verify page count matches expected
- Verify all downloaded images are actual comic pages (no UI/ads)
- Verify sequential naming (page_001 through page_NNN with no gaps)
- Verify metadata.json contains correct information
- Test resume: interrupt and restart, verify it continues from last page

### Edge Cases
- Comic with non-standard aspect ratio (landscape formats)
- Comic with missing pages or gaps in numbering
- Server timeout or network failure mid-download
- Comic with different image hosts (not blogspot)
- Last page duplication (common on readcomiconline)
- Disabled "Next" button detection
- Redirects or popups during navigation

## Acceptance Criteria
- [ ] Script accepts volume name and issue number as command-line arguments
- [ ] Downloads ONLY comic page images (no navigation, ads, or UI elements)
- [ ] Pages are named sequentially: page_001.jpg, page_002.jpg, ..., page_NNN.jpg
- [ ] No gaps in numbering (e.g., no missing page_005)
- [ ] Output organized in `assets/<Volume>/issues/<Issue>/pages/` structure
- [ ] Metadata JSON saved with issue info, page count, and timestamp
- [ ] Can resume interrupted downloads (skips existing pages)
- [ ] Progress indicators match project convention ([OK], [FAIL], [SKIP])
- [ ] Works with at least 3 different comic issues for verification

## Validation Commands
```bash
# Test with Absolute Batman #1
python scripts/scrape_comic_pages.py "Absolute Batman" 1

# Verify output structure
ls -R scripts/assets/Absolute_Batman/issues/1/pages/

# Check all images are valid comic pages (should be ~0.66 aspect ratio)
python -c "
from PIL import Image
import os
for f in os.listdir('scripts/assets/Absolute_Batman/issues/1/pages/'):
    img = Image.open(f'scripts/assets/Absolute_Batman/issues/1/pages/{f}')
    print(f'{f}: {img.size[0]/img.size[1]:.2f} ratio')
"

# Verify metadata exists
cat scripts/assets/Absolute_Batman/issues/1/metadata.json | jq .

# Test resume capability (run twice, should skip existing)
python scripts/scrape_comic_pages.py "Absolute Batman" 1

# Verify no gaps in numbering
ls scripts/assets/Absolute_Batman/issues/1/pages/ | wc -l
# Should match page count in metadata.json
```

## Notes

### Technical Debt
- Current script has hardcoded URL - new script should make URL optional or auto-construct
- No retry logic for failed downloads - consider adding exponential backoff
- No verification that downloaded images match expected hash/size

### Future Enhancements
- Add batch mode: scrape entire volumes at once
- Add ComicVine API integration to auto-fetch issue URLs
- Add progress bar instead of simple print statements
- Add configurable quality settings (different image servers)
- Add support for alternative comic sites if readcomiconline is unavailable

### Dependencies
- Selenium WebDriver (Chrome)
- ChromeDriver (must match Chrome version)
- Python 3.10+ for type hints
- Pillow for image validation (aspect ratio checks)

### Related Features
- `comicvine_download_covers.py` - Volume metadata and cover images
- Remotion pipeline will consume these pages for the "comic slides" view
- D3.js layout integration expects sequential page ordering

### CSS Selector Research Needed
The exact CSS selector for readcomiconline.li comic images must be determined by inspecting the live site. Likely candidates:
- `#mainImage` or `#comicImage` (common naming)
- `.comic-page` or `.page-image` (class-based)
- Specific div container with known ID

Will need to inspect multiple comics to verify selector consistency.
