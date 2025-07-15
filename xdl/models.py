from dataclasses import dataclass
from typing import List

@dataclass
class MediaVariant:
    url: str
    bitrate: int
    content_type: str

@dataclass
class Video:
    id: str
    text: str
    views: int
    likes: int
    rts: int
    replies: int
    created_at: str
    media_variants: List[MediaVariant]

    @property
    def best_mp4(self) -> str:
        vids = [v for v in self.media_variants if v.content_type == "video/mp4"]
        return max(vids, key=lambda v: v.bitrate).url if vids else ""