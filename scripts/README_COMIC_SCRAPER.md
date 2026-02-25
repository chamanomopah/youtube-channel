# Comic Page Scraper

## Overview

The `selenium_webscraping_pages` script downloads comic pages from readcomiconline.li with proper sequential ordering and validation. It follows the project conventions established by `comicvine_download_covers.py`.

## Features

- ✅ **Precise image targeting**: Only downloads actual comic page images (no UI, ads, or navigation elements)
- ✅ **Sequential ordering**: Pages are numbered sequentially (page_001.jpg, page_002.jpg, etc.)
- ✅ **Resume capability**: Can resume interrupted downloads by skipping existing pages
- ✅ **Duplicate detection**: Detects and removes duplicate last pages
- ✅ **Image validation**: Validates aspect ratio and dimensions to ensure only comic pages are downloaded
- ✅ **Metadata tracking**: Saves metadata.json with issue info and page manifest
- ✅ **Project conventions**: Uses same status indicators ([OK], [FAIL], [SKIP]) and directory structure
- ✅ **Issue boundary detection**: Automatically stops at the end of an issue (doesn't leak into next issue)
- ✅ **All issues mode**: Can scrape all issues in a volume automatically

## Installation

Install required dependencies:

```bash
pip install selenium webdriver-manager requests pillow
```

## Usage

### Scraping Modes

#### Single Issue Mode
Scrape only the specified issue:

```bash
python scripts/selenium_webscraping_pages.py "Absolute Batman" 7
```

The script will:
- Download only the pages from Issue #7
- Automatically stop when reaching the next issue
- Respect the page count indicator if available

#### All Issues Mode
Scrape all issues in a volume:

```bash
python scripts/selenium_webscraping_pages.py "Absolute Batman"
```

The script will:
- Start from Issue #1 and continue through all available issues
- Automatically stop when encountering a 404 or no images found
- Create separate folders for each issue

### Advanced Usage

```bash
# Scrape with specific URL
python scripts/selenium_webscraping_pages.py "Absolute Batman" 1 --url "https://readcomiconline.li/Comic/Absolute-Batman/Issue-1?id=234426"

# Run in headless mode (no GUI)
python scripts/selenium_webscraping_pages.py "Absolute Batman" --headless
```

## Output Structure

Files are organized in the following structure:

```
scripts/
└── assets/
    └── <Volume_Name>/
        └── issues/
            └── <Issue_Number>/
                ├── pages/
                │   ├── page_001.jpg
                │   ├── page_002.jpg
                │   ├── page_003.jpg
                │   └── ...
                └── metadata.json
```

### Metadata Format

The `metadata.json` file contains:

```json
{
  "volume": "Absolute Batman",
  "issue": "1",
  "url": "https://readcomiconline.li/Comic/...",
  "total_pages": 42,
  "pages": [
    {
      "page_number": 1,
      "filename": "page_001.jpg",
      "url": "https://...",
      "hash": "abc123..."
    }
  ],
  "scraped_at": "2026-02-25T08:54:00",
  "output_directory": "/path/to/pages"
}
```

## Image Validation

The scraper validates comic pages using:

- **Minimum dimensions**: 500x700 pixels
- **Aspect ratio**: Between 0.5 and 1.5 (standard US comics are ~0.66)
- **File size**: Minimum 10KB
- **Source filtering**: Excludes avatars, icons, ads, banners, buttons

## Resume Capability

If a download is interrupted, simply run the same command again. The scraper will:

1. Detect existing pages in the output directory
2. Resume from the last downloaded page
3. Skip already downloaded files

## Validation

After scraping, you can verify the downloaded pages:

```bash
# Check aspect ratios (should be ~0.66 for standard comics)
python -c "
from PIL import Image
import os
pages_dir = 'scripts/assets/Absolute_Batman/issues/1/pages/'
for f in sorted(os.listdir(pages_dir)):
    img = Image.open(os.path.join(pages_dir, f))
    ratio = img.size[0] / img.size[1]
    print(f'{f}: {img.size[0]}x{img.size[1]} ({ratio:.2f})'
"

# Verify metadata
cat scripts/assets/Absolute_Batman/issues/1/metadata.json | jq .

# Check page count
ls scripts/assets/Absolute_Batman/issues/1/pages/ | wc -l
```

## Troubleshooting

### No comic images found

If you see `[FAIL] No comic image found`:

1. Check that the URL is correct
2. Try running without `--headless` to see what's happening
3. The site may have changed its HTML structure

### Duplicate pages detected

The scraper automatically detects duplicate last pages and stops. This is normal behavior.

### Browser not found

Ensure Chrome browser is installed. The script uses ChromeDriver via webdriver-manager.

### Rate limiting

If you encounter rate limiting:

- Increase `REQUEST_DELAY` in the script
- Run during off-peak hours

## Comparison with Old Script

| Feature | `selenium_webscraping_pages.py` | `selenium_webscraping_pages` |
|---------|--------------------------------|------------------------|
| Command-line args | ❌ Hardcoded URL | ✅ Flexible args |
| Image targeting | ⚠️ All blogspot images >300px | ✅ Precise CSS selectors + validation |
| Directory structure | ❌ Flat `pages/` | ✅ `assets/<Volume>/issues/<Issue>/pages/` |
| Resume capability | ❌ None | ✅ Skips existing pages |
| Metadata | ❌ None | ✅ JSON metadata |
| Duplicate detection | ✅ Basic byte comparison | ✅ Hash-based |
| Progress indicators | ❌ Basic print | ✅ [OK], [FAIL], [SKIP] format |

## Integration with Remotion Pipeline

The scraped pages are designed to work with the Remotion video pipeline:

1. **Grid View**: Display all covers/pages in a grid layout
2. **Timeline View**: Sequential ordering for narrative flow
3. **Comic Slides**: Pages split into panels for detailed viewing
4. **D3.js Integration**: Proper sequential ordering for layout calculations

## Notes

- The scraper respects the site's structure and rate limits
- Consider adding ComicVine API integration for auto-fetching issue URLs (future enhancement)
- Works with any comic volume/issue on readcomiconline.li
- Aspect ratio validation can be adjusted in the configuration section

## See Also

- `comicvine_download_covers.py` - Download volume covers and metadata
- `formato_video_ideial_youtube.md` - Overall video format documentation
