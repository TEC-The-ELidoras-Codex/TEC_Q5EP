#!/usr/bin/env python3
"""
Lyric Extractor (local-first)
-----------------------------
Logs lyric snippets with song metadata (artist, title, album, year) to lyric_log.csv and lyric_log.jsonl.

Usage examples:
  python tools/lyric_extractor.py --snippet "In the distant, in the dark / There's a door of your creation"
  python tools/lyric_extractor.py --snippet "I shine a light into a thousand eyes" --artist "Spiritbox"
  python tools/lyric_extractor.py --use-spotify --snippet "Underneath the gun could you be the one"

What it does:
- Tries (in order) to:
    1) Pull current song from Spotify (if --use-spotify and you have credentials).
    2) Use MusicBrainz to guess song by snippet (and optional --artist, heuristic).
    3) Accept manual "Artist - Title" if you pass --manual "Artist - Title".

Setup (optional for Spotify):
- Create a Spotify app at https://developer.spotify.com/dashboard
- Set env vars: SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI (e.g., http://localhost:8888/callback)
- First run will open a browser to authorize. Token is cached in .cache-lyric-extractor

Notes:
- MusicBrainz is free & open; we only hit their public API, respecting rate limits.
- We do NOT scrape lyrics (copyright). This tool only stores the snippet you provide.
"""

import argparse, csv, datetime as dt, json, os, sys, time, re
from pathlib import Path

try:
    import requests
except Exception:
    print("This script needs the 'requests' package. Install with: pip install requests spotipy", file=sys.stderr)
    raise

# Spotify is optional
try:
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth
    HAVE_SPOTIFY = True
except Exception:
    HAVE_SPOTIFY = False

LOG_CSV = Path("lyric_log.csv")
LOG_JSONL = Path("lyric_log.jsonl")
MB_RATE_SLEEP = 1.1  # be gentle to MusicBrainz


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def musicbrainz_search(snippet: str, artist: str | None = None, limit: int = 5) -> list[dict]:
    out: list[dict] = []
    q = []
    if artist:
        q.append(f'artist:"{artist}"')
    query = " AND ".join(q) if q else "recording:*"
    url = "https://musicbrainz.org/ws/2/recording"
    params = {"query": query, "fmt": "json", "limit": str(limit)}
    try:
        r = requests.get(url, params=params, headers={"User-Agent": "LyricExtractor/0.1 (personal use)"}, timeout=15)
        if r.status_code == 200:
            data = r.json()
            for rec in data.get("recordings", []):
                title = rec.get("title")
                tokens = [t.lower() for t in re.findall(r"[a-zA-Z0-9']+", snippet) if len(t) > 3]
                if title and any(t in title.lower() for t in tokens):
                    artist_credit = ", ".join(ac["artist"]["name"] for ac in rec.get("artist-credit", []))
                    release = None
                    date = None
                    if rec.get("releases"):
                        release = rec["releases"][0].get("title")
                        date = rec["releases"][0].get("date")
                    out.append({
                        "title": title,
                        "artist": artist_credit or None,
                        "album": release,
                        "year": (date or "")[:4] if date else None,
                        "source": "musicbrainz-heuristic",
                        "mbid": rec.get("id")
                    })
            time.sleep(MB_RATE_SLEEP)
    except Exception:
        pass
    return out


def spotify_current_track() -> dict | None:
    if not HAVE_SPOTIFY:
        return None
    try:
        scope = "user-read-currently-playing"
        auth_manager = SpotifyOAuth(scope=scope, cache_path=".cache-lyric-extractor", open_browser=True)
        sp = spotipy.Spotify(auth_manager=auth_manager)
        cur = sp.current_user_playing_track()
        if cur and cur.get("item"):
            item = cur["item"]
            title = item.get("name")
            artist = ", ".join(a["name"] for a in item.get("artists", []))
            album = (item.get("album") or {}).get("name")
            year = None
            release_date = (item.get("album") or {}).get("release_date")
            if release_date:
                year = release_date.split("-")[0]
            url = item.get("external_urls", {}).get("spotify")
            return {"title": title, "artist": artist, "album": album, "year": year, "source": "spotify", "url": url}
    except Exception:
        return None


def parse_manual(manual: str | None) -> dict | None:
    if not manual:
        return None
    if " - " in manual:
        artist, title = manual.split(" - ", 1)
    elif "-" in manual:
        artist, title = manual.split("-", 1)
    else:
        m = re.match(r"(.+?)\s+by\s+(.+)", manual, re.I)
        if m:
            title, artist = m.group(1), m.group(2)
        else:
            return None
    return {"artist": norm(artist), "title": norm(title), "source": "manual"}


def log_entry(row: dict) -> None:
    is_new = not LOG_CSV.exists()
    with LOG_CSV.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if is_new:
            w.writerow(["timestamp", "artist", "title", "album", "year", "source", "url", "snippet"])
        w.writerow([row.get("timestamp"), row.get("artist"), row.get("title"), row.get("album"), row.get("year"), row.get("source"), row.get("url"), row.get("snippet")])
    with LOG_JSONL.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser(description="Log lyric snippets with song metadata (free & local-first).")
    ap.add_argument("--snippet", required=True, help="Lyric snippet you heard")
    ap.add_argument("--artist", help="Optional hint: artist name")
    ap.add_argument("--manual", help='Manual override like "Artist - Title" or "Title by Artist"')
    ap.add_argument("--use-spotify", action="store_true", help="Try reading current track from Spotify")
    args = ap.parse_args()

    snippet = norm(args.snippet)
    now = dt.datetime.now().isoformat(timespec="seconds")

    meta: dict | None = None

    if args.use_spotify:
        meta = spotify_current_track()

    if not meta and args.manual:
        meta = parse_manual(args.manual)

    if not meta:
        candidates = musicbrainz_search(snippet, artist=args.artist, limit=10)
        meta = candidates[0] if candidates else None

    if not meta:
        meta = {"artist": args.artist, "title": None, "album": None, "year": None, "source": "unknown", "url": None}

    row = {
        "timestamp": now,
        "artist": meta.get("artist"),
        "title": meta.get("title"),
        "album": meta.get("album"),
        "year": meta.get("year"),
        "source": meta.get("source"),
        "url": meta.get("url"),
        "snippet": snippet,
    }
    log_entry(row)
    print(json.dumps(row, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
