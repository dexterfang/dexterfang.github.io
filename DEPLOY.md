# Deploy dexterfang.com

## 1. Put the site on GitHub Pages (free, 5 minutes)

1. On github.com (logged in as dexterrrfang) create a new **public** repo named exactly `dexterrrfang.github.io`. Leave it empty (no README).
2. In the terminal, run:

```bash
cd ~/Desktop/Minah/dexter-site && git remote add origin https://github.com/dexterrrfang/dexterrrfang.github.io.git && git branch -M main && git push -u origin main
```

   Git will ask you to sign in once (browser or token).
3. Wait a minute, then open https://dexterrrfang.github.io. Done.
4. Repo → Settings → Actions → General → "Workflow permissions" → **Read and write**. That lets the video refresh job commit new videos every 6 hours.

## 2. Buy the domain

`dexterfang.com` was free to register on 2026-10-06 (checked via whois). Buy it at Cloudflare Registrar (cheapest, no markup) or Namecheap. About $10 a year.

## 3. Point the domain at the site

In the DNS panel of wherever you bought it, add:

| Type  | Name | Value                      |
|-------|------|----------------------------|
| A     | @    | 185.199.108.153            |
| A     | @    | 185.199.109.153            |
| A     | @    | 185.199.110.153            |
| A     | @    | 185.199.111.153            |
| CNAME | www  | dexterrrfang.github.io     |

Then in the GitHub repo → Settings → Pages → Custom domain: `dexterfang.com`, tick "Enforce HTTPS" once it turns green (can take up to an hour).

Tell Claude when the DNS is in and it will add the `CNAME` file and move the old YouTube↔Instagram deep links (dexterrrfang.github.io/go/) onto the new domain.

## Updating later

- Photos / copy: edit `index.html`, commit, push. Pages redeploys in about a minute.
- Latest videos: automatic. The GitHub Action runs `scripts/fetch_videos.py` every 6 hours, pulls the channel RSS, downloads thumbnails, and commits `data/videos.json`. To force it now: repo → Actions → "Refresh latest videos" → Run workflow.
