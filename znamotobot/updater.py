"""Update topic index."""
import asyncio
import logging
from http import HTTPStatus
from pathlib import Path
from pprint import pprint

import aiofiles
from aiohttp import ClientSession, ClientTimeout

from znamotobot import settings
from znamotobot.index import Index
from znamotobot.text_utils import is_http_url

logger = logging.getLogger(__name__)


async def update_index():
    """Download topics and update main index."""
    logger.info("Updating index")
    session = ClientSession(
        timeout=ClientTimeout(total=settings.INDEX_DOWNLOAD_TIMEOUT)
    )
    url = settings.INDEX_URL

    try:
        if is_http_url(url):
            cache_dir = Path(settings.INDEX_CACHE_DIR)
            cache_dir.mkdir(parents=True, exist_ok=True)
            path = str(cache_dir / "index.md")
            await download_file(session, url=url, destination=path)
        else:
            path = url
        settings.INDEX = Index.from_markdown(path)
    finally:
        await session.close()


async def download_file(session: ClientSession, url: str, destination: str):
    logger.debug("GET <%s>", url)
    async with session.get(
        url,
        allow_redirects=True,
    ) as response:
        if response.status == HTTPStatus.OK:
            await save_content(await response.read(), destination)
        else:
            logger.error("Bad status for URL <%s>: %d", url, response.status)


async def save_content(content: bytes, destination: str):
    logger.info("Saving new content <%s>", destination)
    async with aiofiles.open(destination, "wb") as f:
        await f.write(content)


def main():
    asyncio.run(update_index())
    pprint(settings.INDEX)


if __name__ == "__main__":
    main()
