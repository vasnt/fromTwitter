
#!/usr/bin/env python3
"""
Twitter Bookmarks Sync Script
Fetches Twitter bookmarks and updates local markdown file
"""
import os
import sys
import json
from datetime import datetime, timezone

def log(message):
    """Print timestamped log message"""
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    print(f"[{timestamp}] {message}")

def main():
    """Main execution function"""
    log("=" * 60)
    log("Starting Twitter Bookmarks Sync")
    log("=" * 60)

    try:
        # Check for API key
        api_key = os.environ.get('COMPOSIO_API_KEY')
        if not api_key:
            log("✗ ERROR: COMPOSIO_API_KEY not set in environment")
            log("")
            log("Please add it as a GitHub Secret:")
            log("  1. Go to Settings → Secrets and variables → Actions")
            log("  2. Click 'New repository secret'")
            log("  3. Name: COMPOSIO_API_KEY")
            log("  4. Value: Your API key from https://app.composio.dev")
            log("")
            sys.exit(1)

        log("Installing Composio SDK...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "composio-core"], check=True)

        log("Importing Composio SDK...")
        from composio import ComposioToolSet, Action

        log("Initializing Composio client...")
        toolset = ComposioToolSet(api_key=api_key)

        log("Fetching Twitter bookmarks...")
        user_id = os.environ.get('TWITTER_USER_ID', '1675200858425016320')

        # Execute the action
        result = toolset.execute_action(
            action=Action.TWITTER_BOOKMARKS_BY_USER,
            params={
                "id": user_id,
                "max_results": 100
            }
        )

        log(f"API Response received: {type(result)}")

        # Parse response
        if isinstance(result, dict):
            bookmarks = result.get('data', [])
        else:
            bookmarks = []

        if not bookmarks:
            log("⚠ No bookmarks found or unable to parse response")
            log(f"Response: {json.dumps(result, indent=2)[:500]}")
            sys.exit(0)

        log(f"✓ Found {len(bookmarks)} bookmarks")

        # Create markdown
        log("Creating markdown file...")
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

        # Write to file
        output_file = 'twitter_bookmarks.md'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown)

        log(f"✓ Successfully wrote {len(bookmarks)} bookmarks to {output_file}")
        log("=" * 60)
        log("✅ Sync completed successfully!")
        log("=" * 60)

    except ImportError as e:
        log(f"✗ Import Error: {str(e)}")
        log("Failed to import required modules")
        sys.exit(1)
    except Exception as e:
        log(f"✗ FATAL ERROR: {str(e)}")
        import traceback
        log("Traceback:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
