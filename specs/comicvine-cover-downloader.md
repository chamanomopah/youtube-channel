# Plan: Comic Vine Cover Downloader Script

## Task Description
Create a Python script `comicvine_download_covers.py` that uses the Comic Vine API to download all issue covers from a specified volume. The script will be invoked as `py comicvine_download_covers.py "volume name"` and will download cover images in maximum resolution to an organized folder structure.

## Objective
Build a command-line tool that:
1. Searches for a comic volume by name using the Comic Vine API
2. Retrieves all issues associated with that volume
3. Downloads cover images for each issue in maximum resolution
4. Organizes downloaded covers in a structured folder format: `scripts/assets/<Volume_Name>/covers/`
5. Names files using the pattern: `<issue_number>-<issue_name>.<ext>`

## Problem Statement
Currently, there is no automated way to download comic covers from Comic Vine for video production. Manual downloading is time-consuming and error-prone. This script will automate the process of fetching all issue covers for a given volume, ensuring consistent naming and organization for use in Remotion video projects.

## Solution Approach
The script will follow a three-phase workflow:
1. **Volume Search**: Query the Comic Vine `/volumes` endpoint with the volume name filter to find the matching volume
2. **Issue Retrieval**: Fetch all issues for the found volume using the `/issues` endpoint with volume filter
3. **Image Download**: Download cover images from the `image.super_url` field of each issue (highest resolution available)

The solution implements rate limiting (200 requests/hour per Comic Vine API terms), proper error handling, and informative console output.

## Relevant Files

### New Files
- **scripts/comicvine_download_covers.py** - Main script implementation (new file, currently empty)
- **scripts/.env** - Contains `comicvine_api_key` (already exists)

### Supporting Files
- **docs/comicvine_api_docs.md** - API reference for endpoints and field structures

## Implementation Phases

### Phase 1: Foundation
- Set up project structure and imports (requests, pathlib, python-dotenv, urllib)
- Implement environment variable loading for API key
- Create basic argument parsing for volume name input
- Define constants and configuration (API base URL, output directory)

### Phase 2: Core Implementation
- Implement volume search function using `/volumes` endpoint with filter
- Implement issue listing function using `/issues` endpoint with volume filter
- Implement pagination handling to fetch all issues (API limits to 100 per page)
- Implement cover image download function with proper error handling
- Implement filename sanitization for valid file paths

### Phase 3: Integration & Polish
- Create main execution flow with progress indicators
- Add rate limiting to respect API terms (200 requests/hour)
- Implement comprehensive error handling (network errors, API errors, missing data)
- Add detailed console logging for user feedback
- Handle edge cases (no results found, missing covers, duplicate issue numbers)

## Step by Step Tasks

### 1. Project Setup and Dependencies
- Create Python script with shebang and encoding declaration
- Import required libraries: `sys`, `os`, `pathlib`, `requests`, `dotenv`, `time`, `re`
- Load COMICVINE_API_KEY from `.env` file
- Define API base URL: `https://comicvine.gamespot.com/api`
- Define output base path: `scripts/assets/`

### 2. Volume Search Function
- Create `search_volume(volume_name: str) -> dict or None` function
- Construct API request to `/volumes` endpoint with:
  - `filter=name:<volume_name>` for exact name matching
  - `field_list=id,name,publisher,start_year,count_of_issues` to minimize response size
  - `format=json`
  - `api_key=<key>`
- Handle API response and check `status_code` (1 = OK)
- Return first result if found, None otherwise
- Print search results with volume details for user confirmation

### 3. Issue List Function with Pagination
- Create `get_volume_issues(volume_id: int) -> list[dict]` function
- Initialize empty issues list and offset counter
- Loop while True:
  - Request `/issues` endpoint with:
    - `filter=volume:<volume_id>`
    - `field_list=id,issue_number,name,image,cover_date`
    - `limit=100` (max allowed)
    - `offset=<current_offset>`
  - Append results to issues list
  - Break if `number_of_page_results` < 100 (last page)
  - Increment offset by 100
  - Sleep briefly to respect rate limits
- Return complete list of issues sorted by issue_number

### 4. Filename Sanitization
- Create `sanitize_filename(name: str) -> str` function
- Replace invalid characters: `/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`
- Replace spaces and multiple underscores with single underscore
- Strip leading/trailing spaces and underscores
- Limit length to 255 characters (filesystem limit)

### 5. Cover Download Function
- Create `download_cover(issue: dict, output_dir: Path) -> bool` function
- Extract issue data:
  - `issue_number` from `issue['issue_number']`
  - `issue_name` from `issue['name']` or "Unnamed"
  - Cover URL from `issue['image']['super_url']` (highest resolution)
- Sanitize issue name for filename
- Construct filename: `{issue_number}-{sanitized_name}.jpg` (extract extension from URL)
- Create full output path
- Skip if file already exists
- Download image with streaming to handle large files
- Save file with error handling
- Print progress indicator (✓ for success, ✗ for failure)
- Return True on success, False on failure

### 6. Main Execution Flow
- Create `main()` function
- Parse command-line argument for volume name
- Call `search_volume()` and exit if not found
- Create output directory: `assets/<sanitized_volume_name>/covers/`
- Call `get_volume_issues()` to get all issues
- Print summary: "Found X issues for <volume_name>"
- Iterate through issues and call `download_cover()` for each
- Track successful/failed downloads
- Print final summary with statistics

### 7. Error Handling and Edge Cases
- Handle missing API key (check if empty after loading)
- Handle volume not found (print message and exit)
- Handle empty issue list (warning message)
- Handle missing cover images (skip and log warning)
- Handle network errors (retry with backoff or skip)
- Handle filesystem errors (permission issues, disk space)
- Add `--help` argument for usage instructions
- Validate volume name argument is provided

### 8. Rate Limiting and Performance
- Implement 1-second delay between API requests (well within 200/hour limit)
- Use session pooling for HTTP requests (requests.Session())
- Show progress bar or percentage for downloads
- Implement early termination on Ctrl+C (graceful shutdown)

## Testing Strategy

### Unit Testing (Optional)
- Test filename sanitization with various edge cases
- Test URL construction and parameter encoding

### Integration Testing
- Test with known volume: "Absolute Batman" (should have 17 issues)
- Test with volume containing special characters in name
- Test with missing API key (should fail gracefully)
- Test re-running script (should skip existing files)
- Test with volume that has no issues

### Edge Cases to Validate
- Volume name not found in API
- Issue with missing name field
- Issue with missing image field
- Issue numbers as decimals (e.g., "1.5", "½")
- Very long issue names
- Network timeout during download
- Insufficient disk space

## Acceptance Criteria

The script is complete when:
1. ✅ Running `py comicvine_download_covers.py "Absolute Batman"` downloads all 17 issue covers
2. ✅ Files are saved to `scripts/assets/Absolute_Batman/covers/`
3. ✅ Files follow naming pattern: `1-The_Zoo_Part_One.jpg`, `2-The_Zoo_Part_Two.jpg`, etc.
4. ✅ Covers are downloaded in maximum resolution (from `super_url`)
5. ✅ Script handles missing volumes gracefully with error message
6. ✅ Script skips already-downloaded files on re-run
7. ✅ Progress indicators show download status
8. ✅ Final summary shows successful/failed counts
9. ✅ API rate limits are respected (no blocks)
10. ✅ Special characters in names are sanitized properly

## Validation Commands

```bash
# Test with Absolute Batman volume (known to have 17 issues)
py scripts/comicvine_download_covers.py "Absolute Batman"

# Verify output structure
ls -la scripts/assets/Absolute_Batman/covers/

# Check file count (should be 17 for Absolute Batman)
ls scripts/assets/Absolute_Batman/covers/ | wc -l

# Verify image files are valid (not corrupted)
file scripts/assets/Absolute_Batman/covers/*.jpg

# Test help message
py scripts/comicvine_download_covers.py --help
```

## Notes

### API Rate Limiting
- Comic Vine allows 200 requests per resource per hour
- Implement 1-second delay between requests for safety
- Cache responses where possible to minimize redundant calls

### Image URLs Available
From the API documentation, each issue has an `image` object with:
- `icon_url` - Smallest size
- `medium_url` - Medium size
- `screen_url` - Screen size
- `screen_large_url` - Large screen size
- `super_url` - **Maximum resolution** (use this one)

### Dependencies
The script requires:
- `requests` - HTTP library for API calls
- `python-dotenv` - Environment variable loading

Install with:
```bash
pip install requests python-dotenv
```

Or if using UV:
```bash
uv add requests python-dotenv
```

### Future Enhancements
- Add `--force` flag to re-download existing files
- Add `--output` flag to specify custom output directory
- Add JSON export of issue metadata alongside images
- Add progress bar with `tqdm` library
- Support downloading variant covers (if available in API)
- Batch processing for multiple volumes

### Comic Vine API Terms Compliance
- Non-commercial use only
- Must link back to Comic Vine on any page using data
- Cannot redistribute data in another form
- Cannot build competing products
- API key: Stored in `.env` file (already exists)

### Example Expected Output Structure
```
scripts/assets/Absolute_Batman/
└── covers/
    ├── 1-The_Zoo_Part_One.jpg
    ├── 2-The_Zoo_Part_Two.jpg
    ├── 3-The_Zoo_Part_Three.jpg
    ├── 4-The_Zoo_Part_Four.jpg
    ├── 5-The_Zoo_Part_Five.jpg
    ├── 6-The_Zoo_Part_Six.jpg
    ├── 7-The_Georgia_Short_Flash_Part_One.jpg
    ├── 8-The_Georgia_Short_Flash_Part_Two.jpg
    ├── 9-The_Georgia_Short_Flash_Part_Three.jpg
    ├── 10-The_Georgia_Short_Flash_Part_Four.jpg
    ├── 11-The_Georgia_Short_Flash_Part_Five.jpg
    ├── 12-Executive_Assistant_In mourning.jpg
    ├── 13-Executive_Assistant_In mourning_Part_Two.jpg
    ├── 14-Executive_Assistant_In mourning_Part_Three.jpg
    ├── 15-Executive_Assistant_In mourning_Part_Four.jpg
    ├── 16-The_Time_Of_the_Dragon_Part_One.jpg
    └── 17-The_Time_Of_the_Dragon_Part_Two.jpg
```
