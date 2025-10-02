#!/usr/bin/env python3
import os
import json
import requests
from datetime import datetime

# Configuration
COMPOSIO_API_KEY = os.environ.get('COMPOSIO_API_KEY')
TWITTER_USER_ID = os.environ.get('TWITTER_USER_ID', '1675200858425016320')
COMPOSIO_API_URL = "https://backend.composio.dev/api/v1/actions"

def execute_composio_tool(tool_name, parameters):
    """Execute a Composio tool via API"""
    headers = {
        "X-API-Key": COMPOSIO_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "actionName": tool_name,
        "params": parameters
    }

    response = requests.post(
        f"{COMPOSIO_API_URL}/{tool_name}/execute",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

def fetch_twitter_bookmarks():
    """Fetch all Twitter bookmarks"""
    print("Fetching Twitter bookmarks...")

    result = execute_composio_tool(
        "TWITTER_BOOKMARKS_BY_USER",
        {
            "id": TWITTER_USER_ID,
            "max_results": 100
        }
    )

    bookmarks = result.get('data', {}).get('data', [])
    print(f"Found {len(bookmarks)} bookmarks")
    return bookmarks

def create_markdown_content(bookmarks):
    """Create markdown content from bookmarks"""
    markdown = f"""# Twitter Bookmarks

**Total Bookmarks:** {len(bookmarks)}  
**Last Updated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC

---

"""

    for i, bookmark in enumerate(bookmarks, 1):
        tweet_id = bookmark.get('id', '')
        text = bookmark.get('text', '').replace('\n', ' ').strip()
        tweet_url = f"https://twitter.com/i/web/status/{tweet_id}"

        markdown += f"""### {text}

**Tweet ID:** `{tweet_id}`  
**Link:** [{tweet_url}]({tweet_url})

---

"""

    return markdown

def main():
    print("Starting Twitter bookmarks sync...")

    if not COMPOSIO_API_KEY:
        print("ERROR: COMPOSIO_API_KEY not set")
        return

    try:
        # Fetch bookmarks
        bookmarks = fetch_twitter_bookmarks()

        # Create markdown
        markdown_content = create_markdown_content(bookmarks)

        # Write to file
        with open('twitter_bookmarks.md', 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        print(f"✅ Successfully synced {len(bookmarks)} bookmarks!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
