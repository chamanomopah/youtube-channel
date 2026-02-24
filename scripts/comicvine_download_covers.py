#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comic Vine Cover Downloader

Downloads all issue covers from a specified comic volume using the Comic Vine API.
Usage: python comicvine_download_covers.py "Volume Name"
"""

import sys
import os
import re
import time
from pathlib import Path
from urllib.parse import urlparse

try:
    import requests
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Error: Missing required dependency: {e}")
    print("Install with: pip install requests python-dotenv")
    sys.exit(1)


# Configuration
API_BASE_URL = "https://comicvine.gamespot.com/api"
# Path is relative to project root (parent of scripts directory)
SCRIPT_DIR = Path(__file__).parent
OUTPUT_BASE_PATH = SCRIPT_DIR / "assets"
REQUEST_DELAY = 1.0  # Seconds between API requests (respects 200/hour limit)

# HTTP Headers required by Comic Vine API
HEADERS = {
    "User-Agent": "ComicVineCoverDownloader/1.0 (Python; Comic Vine API Client)"
}


def load_api_key():
    """Load Comic Vine API key from .env file."""
    env_path = Path(__file__).parent / ".env"
    load_dotenv(env_path)
    api_key = os.getenv("comicvine_api_key")
    if not api_key:
        print("Error: COMICVINE_API_KEY not found in .env file")
        sys.exit(1)
    return api_key


def sanitize_filename(name: str) -> str:
    """
    Sanitize a string for use as a filename.

    Replaces invalid filesystem characters and limits length.
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


def search_volume(volume_name: str, api_key: str, session: requests.Session) -> dict | None:
    """
    Search for a comic volume by name using the Comic Vine API.

    Args:
        volume_name: Name of the volume to search for
        api_key: Comic Vine API key
        session: Requests session for connection pooling

    Returns:
        Volume dictionary if found, None otherwise
    """
    print(f"Searching for volume: {volume_name}")

    params = {
        "filter": f"name:{volume_name}",
        "field_list": "id,name,publisher,start_year,count_of_issues",
        "format": "json",
        "api_key": api_key
    }

    try:
        response = session.get(f"{API_BASE_URL}/volumes", params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("status_code") != 1:
            print(f"API Error: {data.get('error', 'Unknown error')}")
            return None

        results = data.get("results", [])
        if not results:
            print(f"No volume found with name: {volume_name}")
            return None

        # Try to find exact match first
        volume = None
        for result in results:
            if result["name"].lower() == volume_name.lower():
                volume = result
                break

        # If no exact match, use first result
        if not volume:
            volume = results[0]
            print(f"Note: Exact match not found. Using closest match.")

        print(f"Found: {volume['name']} ({volume.get('start_year', 'N/A')})")
        print(f"Publisher: {volume.get('publisher', {}).get('name', 'Unknown')}")
        print(f"Issues: {volume.get('count_of_issues', 'Unknown')}")

        return volume

    except requests.RequestException as e:
        print(f"Error searching for volume: {e}")
        return None


def get_volume_issues(volume_id: int, api_key: str, session: requests.Session) -> list[dict]:
    """
    Retrieve all issues for a given volume using pagination.

    Args:
        volume_id: Comic Vine volume ID
        api_key: Comic Vine API key
        session: Requests session for connection pooling

    Returns:
        List of issue dictionaries sorted by issue_number
    """
    issues = []
    offset = 0
    limit = 100

    print(f"Fetching issues for volume ID: {volume_id}")

    while True:
        params = {
            "filter": f"volume:{volume_id}",
            "field_list": "id,issue_number,name,image,cover_date",
            "format": "json",
            "limit": limit,
            "offset": offset,
            "api_key": api_key
        }

        try:
            response = session.get(f"{API_BASE_URL}/issues", params=params)
            response.raise_for_status()
            data = response.json()

            if data.get("status_code") != 1:
                print(f"API Error: {data.get('error', 'Unknown error')}")
                break

            page_results = data.get("results", [])
            issues.extend(page_results)

            # Check if we've fetched all issues
            if len(page_results) < limit:
                break

            offset += limit
            print(f"Fetched {len(issues)} issues so far...")
            time.sleep(REQUEST_DELAY)

        except requests.RequestException as e:
            print(f"Error fetching issues: {e}")
            break

    # Sort by issue_number
    try:
        issues.sort(key=lambda x: float(x.get("issue_number", 0)))
    except (ValueError, TypeError):
        # If issue_number is not numeric, keep original order
        pass

    return issues


def download_cover(issue: dict, output_dir: Path, session: requests.Session) -> bool:
    """
    Download a single issue cover image.

    Args:
        issue: Issue dictionary from Comic Vine API
        output_dir: Directory to save the cover image
        session: Requests session for connection pooling

    Returns:
        True if download successful, False otherwise
    """
    # Extract issue data
    issue_number = issue.get("issue_number", "Unknown")
    issue_name = issue.get("name") or "Unnamed"

    # Get cover URL (super_url is highest resolution)
    image_data = issue.get("image", {})
    cover_url = image_data.get("super_url")

    if not cover_url:
        print(f"[FAIL] Issue {issue_number}: No cover image available")
        return False

    # Sanitize issue name for filename
    sanitized_name = sanitize_filename(issue_name)

    # Get file extension from URL
    parsed_url = urlparse(cover_url)
    ext = os.path.splitext(parsed_url.path)[1] or ".jpg"

    # Construct filename
    filename = f"{issue_number}-{sanitized_name}{ext}"
    output_path = output_dir / filename

    # Skip if file already exists
    if output_path.exists():
        print(f"[SKIP] Issue {issue_number}: Already downloaded")
        return True

    # Download image
    try:
        response = session.get(cover_url, stream=True)
        response.raise_for_status()

        # Create parent directories if they don't exist
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save file
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"[OK] Issue {issue_number}: Downloaded")
        return True

    except requests.RequestException as e:
        print(f"[FAIL] Issue {issue_number}: Download failed - {e}")
        return False
    except (IOError, OSError) as e:
        print(f"[FAIL] Issue {issue_number}: File save failed - {e}")
        return False


def main():
    """Main execution flow."""
    # Parse command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python comicvine_download_covers.py <volume_name>")
        print("Example: python comicvine_download_covers.py \"Absolute Batman\"")
        sys.exit(1)

    if sys.argv[1] in ["--help", "-h"]:
        print("Comic Vine Cover Downloader")
        print("\nUsage:")
        print("  python comicvine_download_covers.py <volume_name>")
        print("\nExample:")
        print("  python comicvine_download_covers.py \"Absolute Batman\"")
        print("\nDescription:")
        print("  Downloads all issue covers for a given comic volume from Comic Vine.")
        print("  Covers are saved to scripts/assets/<Volume_Name>/covers/")
        sys.exit(0)

    volume_name = sys.argv[1]

    # Load API key
    api_key = load_api_key()

    # Create requests session for connection pooling
    session = requests.Session()
    session.headers.update(HEADERS)

    # Search for volume
    volume = search_volume(volume_name, api_key, session)
    if not volume:
        sys.exit(1)

    # Create output directory
    sanitized_volume_name = sanitize_filename(volume["name"])
    output_dir = OUTPUT_BASE_PATH / sanitized_volume_name / "covers"

    # Get all issues
    issues = get_volume_issues(volume["id"], api_key, session)
    time.sleep(REQUEST_DELAY)

    if not issues:
        print(f"Warning: No issues found for volume: {volume_name}")
        sys.exit(0)

    print(f"\nFound {len(issues)} issues for {volume_name}")
    print(f"Output directory: {output_dir}\n")

    # Download covers
    success_count = 0
    failure_count = 0
    skip_count = 0

    for i, issue in enumerate(issues, 1):
        print(f"[{i}/{len(issues)}] ", end="")

        result = download_cover(issue, output_dir, session)

        if result:
            success_count += 1
        else:
            failure_count += 1

        # Rate limiting for downloads
        time.sleep(REQUEST_DELAY / 2)

    # Print summary
    print("\n" + "=" * 50)
    print("Download Summary")
    print("=" * 50)
    print(f"Total issues: {len(issues)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {failure_count}")
    print(f"Output directory: {output_dir.absolute()}")
    print("=" * 50)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDownload cancelled by user.")
        sys.exit(0)
