#!/usr/bin/env python3
"""Refresh data/videos.json from the channel's public RSS feed (no API key needed) and
download thumbnails into assets/yt/ so the page never hotlinks YouTube.
Run: python3 scripts/fetch_videos.py   (GitHub Action runs it every 6 hours)"""
import json, os, re, sys, urllib.request, xml.etree.ElementTree as ET

CHANNEL_ID = os.environ.get("YOUTUBE_CHANNEL_ID", "UC7sKibs5R5NZ4Lp3VD_VxrQ")  # @dexter_fang
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "videos.json")
THUMBS = os.path.join(ROOT, "assets", "yt")
NS = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015", "m": "http://search.yahoo.com/mrss/"}
UA = {"User-Agent": "Mozilla/5.0 (dexterfang.com video refresh)"}

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()

feed = ET.fromstring(get(f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"))
videos = []
for e in feed.findall("a:entry", NS):
    vid = e.find("yt:videoId", NS).text
    title = e.find("a:title", NS).text
    published = e.find("a:published", NS).text
    videos.append({"id": vid, "title": title, "published": published,
                   "thumb": f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"})
videos.sort(key=lambda v: v["published"], reverse=True)

# Shorts have no reliable flag in RSS; keep everything, the page shows the first four.
os.makedirs(THUMBS, exist_ok=True)
keep = videos[:8]
for v in keep:
    path = os.path.join(THUMBS, f"{v['id']}.jpg")
    if not os.path.exists(path):
        for cand in (f"https://i.ytimg.com/vi/{v['id']}/maxresdefault.jpg", v["thumb"]):
            try:
                data = get(cand)
                if len(data) > 5000:
                    open(path, "wb").write(data); break
            except Exception:
                pass
    v["thumb_local"] = f"assets/yt/{v['id']}.jpg" if os.path.exists(path) else v["thumb"]

old = open(OUT).read() if os.path.exists(OUT) else ""
new = json.dumps({"channel": CHANNEL_ID, "videos": keep}, indent=1, ensure_ascii=False)
if new != old:
    open(OUT, "w").write(new)
    print(f"updated {OUT}: {len(keep)} videos, newest {keep[0]['title']!r}")
else:
    print("no change")
