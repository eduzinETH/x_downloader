import asyncio
import typer
import pandas as pd
import rich
from dotenv import load_dotenv
from .client import XClient
from .metrics import to_dataframe
from .downloader import download_many

load_dotenv()

app = typer.Typer(help="CLI para listar, rankear e baixar vídeos do X.com")

@app.command()
def list(username: str):
    """Lista os 50 vídeos mais recentes."""
    df = asyncio.run(_collect(username))
    rich.print(df.head())

@app.command()
def rank(username: str, metric: str = typer.Option("views", "--by")):
    """Mostra ranking pelo métrica escolhida."""
    df = asyncio.run(_collect(username))
    df = df.sort_values(metric, ascending=False)
    rich.print(df[["id", "text", metric]].head(10))

@app.command()
def download(username: str):
    """Baixa vídeos por ordem de visualização."""
    df = asyncio.run(_collect(username))
    urls = df.sort_values("views", ascending=False)["url"].tolist()
    asyncio.run(download_many(urls))

async def _collect(username: str):
    async with XClient() as cli:
        uid = await cli.get_user_id(username)
        vids = await cli.fetch_videos(uid)
    return to_dataframe(vids)

if __name__ == "__main__":
    app()