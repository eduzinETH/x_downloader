import pandas as pd
from typing import List, Dict

def to_dataframe(videos: List[Dict]) -> pd.DataFrame:
    df = pd.DataFrame(videos)
    return df[["id", "text", "views", "likes", "rts", "replies", "created_at", "url"]]