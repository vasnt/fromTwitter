#!/usr/bin/env python3
import os
import sys
import json
import requests
from datetime import datetime, timezone

def log(msg):
    print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] {msg}")

def main():
    log("=" * 60)
    log("Twitter Bookmarks Sync Started")
    log("=" * 60)

    # Check API key
    api_key = os.environ.get('COMPOSIO_API_KEY')
    if not api_key:
        log("ERROR: COMPOSIO_API_KEY not found!")
        log("Add it at: Settings → Secrets and variables → Actions")
        sys.exit(1)

    user_id = os.environ.get('TWITTER_USER_ID', '1675200858425016320')
    log(f"User ID: {user_id}")

    # Call Composio API directly
    url = "https://backend.composio.dev/api/v1/actions/TWITTER_BOOKMARKS_BY_USER/execute"
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "input": {
            "id": user_id,
            "max_results": 100
        }
    }

    log("Fetching bookmarks from Twitter...")
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        log(f"Response status: {response.status_code}")

        if response.status_code != 200:
            log(f"ERROR: API returned {response.status_code}")
            log(f"Response: {response.text[:500]}")
            sys.exit(1)

        result = response.json()
        log(f"Response received: {len(str(result))} chars")

        # Extract bookmarks - handle various response structures
        bookmarks = []

        # Try different paths where data might be
        if 'data' in result:
            if isinstance(result['data'], list):
                bookmarks = result['data']
            elif isinstance(result['data'], dict):
                if 'data' in result['data']:
                    bookmarks = result['data']['data']
                elif 'bookmarks' in result['data']:
                    bookmarks = result['data']['bookmarks']

        # Try execution_details path
        if not bookmarks and 'execution_details' in result:
            exec_resp = result['execution_details'].get('executed_response', {})
            if 'data' in exec_resp:
                bookmarks = exec_resp['data']

        if not bookmarks:
            log(f"WARNING: No bookmarks found in response")
            log(f"Response structure: {json.dumps(result, indent=2)[:1000]}")
            sys.exit(0)

        log(f"✓ Found {len(bookmarks)} bookmarks")

        # Create markdown
        now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        markdown = f'''# Twitter Bookmarks

**Total Bookmarks:** {len(bookmarks)}  
**Last Updated:** {now} UTC

---

'''

        for bookmark in bookmarks:
            tweet_id = bookmark.get('id', '')
            text = bookmark.get('text', '').replace('\n', ' ').strip()
            url = f"https://twitter.com/i/web/status/{tweet_id}"

            markdown += f'''### {text}

**Tweet ID:** `{tweet_id}`  
**Link:** [{url}]({url})

---

'''

        # Write file
        with open('twitter_bookmarks.md', 'w', encoding='utf-8') as f:
            f.write(markdown)

        log(f"✓ Wrote {len(bookmarks)} bookmarks to twitter_bookmarks.md")
        log("=" * 60)
        log("✅ Sync completed successfully!")
        log("=" * 60)

    except requests.exceptions.RequestException as e:
        log(f"ERROR: Network request failed: {e}")
        sys.exit(1)
    except Exception as e:
        log(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
