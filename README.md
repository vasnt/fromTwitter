# Twitter Bookmarks Auto-Sync

Automatically syncs your Twitter bookmarks to this GitHub repository every 6 hours.

## 📋 Setup Instructions

To enable automatic syncing, you need to add your Composio API key as a GitHub secret:

### Step 1: Get Your Composio API Key

1. Go to [Composio Dashboard](https://app.composio.dev)
2. Navigate to Settings → API Keys
3. Copy your API key

### Step 2: Add Secret to GitHub

1. Go to your repository settings: [fromTwitter Settings](https://github.com/vasnt/fromTwitter/settings/secrets/actions)
2. Click **"New repository secret"**
3. Set:
   - **Name:** `COMPOSIO_API_KEY`
   - **Value:** (paste your Composio API key)
4. Click **"Add secret"**

### Step 3: Enable GitHub Actions

1. Go to the [Actions tab](https://github.com/vasnt/fromTwitter/actions)
2. If prompted, click **"I understand my workflows, go ahead and enable them"**

## ⚙️ How It Works

- **Automated Sync:** Runs every 6 hours automatically
- **Manual Trigger:** You can also trigger sync manually from the Actions tab
- **Smart Updates:** Only commits changes if new bookmarks are detected

## 🔄 Sync Schedule

The workflow runs automatically:
- Every 6 hours (00:00, 06:00, 12:00, 18:00 UTC)
- Or manually via the Actions tab

### Adjusting Schedule

To change the sync frequency, edit `.github/workflows/sync-bookmarks.yml`:

```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
```

Common schedules:
- Every hour: `0 * * * *`
- Every 3 hours: `0 */3 * * *`
- Every 12 hours: `0 */12 * * *`
- Daily at midnight: `0 0 * * *`

## 📊 Current Stats

**Total Bookmarks:** 99  
**Last Updated:** Check the latest commit

## 🔗 Files

- [`twitter_bookmarks.md`](twitter_bookmarks.md) - Your synced bookmarks
- [`.github/workflows/sync-bookmarks.yml`](.github/workflows/sync-bookmarks.yml) - GitHub Actions workflow
- [`sync_bookmarks.py`](sync_bookmarks.py) - Sync script

## 🚀 Manual Sync

To manually trigger a sync:

1. Go to [Actions → Sync Twitter Bookmarks](https://github.com/vasnt/fromTwitter/actions/workflows/sync-bookmarks.yml)
2. Click **"Run workflow"**
3. Click the green **"Run workflow"** button

## 📝 Notes

- The workflow requires your Twitter account to be connected to Composio
- Bookmarks are fetched in batches of 100 (Twitter API limit)
- Full tweet content is preserved in titles for easy browsing
- All syncs are logged in the Actions tab

## 🔐 Security

- Your Composio API key is stored securely as a GitHub secret
- Never commit API keys directly to the repository
- The workflow only has access to this repository

---

**Need help?** Check the [Actions logs](https://github.com/vasnt/fromTwitter/actions) for any errors.
