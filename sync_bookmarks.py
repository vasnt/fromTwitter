#!/usr/bin/env python3
"""
Twitter Bookmarks Sync Script
Fetches Twitter bookmarks via Composio API and updates local markdown file
"""
import os
import sys
import json
import requests
from datetime import datetime, timezone

# Configuration
COMPOSIO_API_KEY = os.environ.get('COMPOSIO_API_KEY')
TWITTER_USER_ID = os.environ.get('TWITTER_USER_ID', '1675200858425016320')
COMPOSIO_BASE_URL = "https://backend.composio.dev/api/v1"

def log(message):
    """Print timestamped log message"""
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    print(f"[{timestamp}] {message}")

def execute_composio_tool(action_name, parameters):
    """Execute a Composio action via API"""
    if not COMPOSIO_API_KEY:
        raise Exception("COMPOSIO_API_KEY environment variable is not set")

    url = f"{COMPOSIO_BASE_URL}/actions/{action_name}/execute"
    headers = {
        "X-API-Key": COMPOSIO_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "input": parameters
    }

    log(f"Calling Composio API: {action_name}")
    response = requests.post(url, headers=headers, json=payload, timeout=30)

    if response.status_code != 200:
        raise Exception(f"API Error {response.status_code}: {response.text}")

    result = response.json()

    # Check for execution errors
    if not result.get('successfull', True):
        error_msg = result.get('error', 'Unknown error')
        raise Exception(f"Execution failed: {error_msg}")

    return result

def fetch_twitter_bookmarks():
    """Fetch all Twitter bookmarks"""
    log("Fetching Twitter bookmarks...")

    try:
        result = execute_composio_tool(
            "TWITTER_BOOKMARKS_BY_USER",
            {
                "id": TWITTER_USER_ID,
                "max_results": 100
            }
        )

        # Extract bookmarks from response
        execution_details = result.get('execution_details', {})
        executed_response = execution_details.get('executed_response', {})
        bookmarks_data = executed_response.get('data', [])

        log(f"✓ Found {len(bookmarks_data)} bookmarks")
        return bookmarks_data

    except Exception as e:
        log(f"✗ Error fetching bookmarks: {str(e)}")
        raise

def create_markdown_content(bookmarks):
    """Create markdown content from bookmarks"""
    now_utc = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    markdown = f'''# Twitter Bookmarks

**Total Bookmarks:** {len(bookmarks)}  
**Last Updated:** {now_utc} UTC

---

'''

    for bookmark in bookmarks:
        tweet_id = bookmark.get('id', '')
        text = bookmark.get('text', '').replace('\n', ' ').strip()
        tweet_url = f"https://twitter.com/i/web/status/{tweet_id}"

        markdown += f'''### {text}

**Tweet ID:** `{tweet_id}`  
**Link:** [{tweet_url}]({tweet_url})

---

'''

    return markdown

def main():
    """Main execution function"""
    log("=" * 60)
    log("Starting Twitter Bookmarks Sync")
    log("=" * 60)

    try:
        # Check API key
        if not COMPOSIO_API_KEY:
            log("✗ ERROR: COMPOSIO_API_KEY not set in environment")
            log("Please add it as a GitHub Secret:")
            log("  1. Go to Settings → Secrets and variables → Actions")
            log("  2. Add COMPOSIO_API_KEY with your API key")
            sys.exit(1)

        # Fetch bookmarks
        bookmarks = fetch_twitter_bookmarks()

        if not bookmarks:
            log("⚠ No bookmarks found")
            sys.exit(0)

        # Create markdown
        log("Creating markdown file...")
        markdown_content = create_markdown_content(bookmarks)

        # Write to file
        output_file = 'twitter_bookmarks.md'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        log(f"✓ Successfully wrote {len(bookmarks)} bookmarks to {output_file}")
        log("=" * 60)
        log("Sync completed successfully!")
        log("=" * 60)

    except Exception as e:
        log(f"✗ FATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
