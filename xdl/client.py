import os
import httpx
import asyncio
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

BASE = "https://api.twitter.com/2"
HEADERS = {"Authorization": f"Bearer {os.getenv('X_BEARER')}"}

class XClient:
    def __init__(self, timeout: int = 30):
        self._timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        self._client = httpx.AsyncClient(timeout=self._timeout, headers=HEADERS)
        return self

    async def __aexit__(self, *exc):
        await self._client.aclose()

    async def get_user_id(self, username: str) -> str:
        url = f"{BASE}/users/by/username/{username}"
        r = await self._client.get(url)
        r.raise_for_status()
        return r.json()["data"]["id"]

    async def fetch_videos(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        url = f"{BASE}/users/{user_id}/tweets"
        params = {
            "max_results": min(limit, 100),
            "tweet.fields": "public_metrics,created_at,attachments",
            "expansions": "attachments.media_keys",
            "media.fields": "type,url,variants"
        }

        r = await self._client.get(url, params=params)
        r.raise_for_status()
        data = r.json()

        tweets = data.get("data", [])
        includes = data.get("includes", {})
        medias = {m["media_key"]: m for m in includes.get("media", []) if m["type"] == "video"}

        results = []
        for tweet in tweets:
            media_keys = tweet.get("attachments", {}).get("media_keys", [])
            for key in media_keys:
                media = medias.get(key)
                if media:
                    video_url = ""
                    # Busca a maior qualidade do vídeo
                    variants = media.get("variants", [])
                    mp4_variants = [v for v in variants if v.get("content_type") == "video/mp4"]
                    if mp4_variants:
                        mp4_variants.sort(key=lambda x: x.get("bit_rate", 0), reverse=True)
                        video_url = mp4_variants[0]["url"]

                    metrics = tweet.get("public_metrics", {})
                    results.append({
                        "id": tweet["id"],
                        "text": tweet["text"],
                        "views": metrics.get("view_count", 0),
                        "likes": metrics.get("like_count", 0),
                        "rts": metrics.get("retweet_count", 0),
                        "replies": metrics.get("reply_count", 0),
                        "created_at": tweet["created_at"],
                        "url": video_url
                    })

        return results
