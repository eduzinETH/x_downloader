import aiohttp
import asyncio
import pathlib
import tqdm.asyncio as tq

async def _download(session: aiohttp.ClientSession, url: str, dest: pathlib.Path):
    async with session.get(url) as r:
        r.raise_for_status()
        dest.write_bytes(await r.read())

async def download_many(urls: list[str], out_dir: str = "downloads"):
    path = pathlib.Path(out_dir)
    path.mkdir(exist_ok=True)
    async with aiohttp.ClientSession() as session:
        tasks = [_download(session, u, path / f"{i:02}.mp4") for i, u in enumerate(urls, start=1)]
        for f in tq.tqdm.as_completed(tasks):
            await f