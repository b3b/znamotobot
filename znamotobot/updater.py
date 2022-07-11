"""Update topic index."""
import asyncio
import logging
from http import HTTPStatus
from pathlib import Path
from pprint import pprint

import aiofiles
from aiohttp import ClientError, ClientSession, ClientTimeout

from znamotobot import settings
from znamotobot.index import Index
from znamotobot.text_utils import is_http_url

logger = logging.getLogger(__name__)


class IndexUpdater:
    """Class for periodic updating of topics index."""

    def __init__(self):
        self.timeout = settings.INDEX_DOWNLOAD_TIMEOUT
        self.url = settings.INDEX_URL
        self.update_period = settings.INDEX_UPDATE_PERIOD
        self.cache_dir = Path(settings.INDEX_CACHE_DIR)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._session: ClientSession = None

    @property
    def session(self) -> ClientSession:
        if not self._session:
            self._session = ClientSession(timeout=ClientTimeout(total=self.timeout))
        return self._session

    async def start(self):
        """Start polling for updates."""
        try:
            await self._run_polling()
        except asyncio.CancelledError:
            logger.info("Stop index updater")
        except Exception as exc:
            logger.error("Updater exit on error", exc_info=exc)
            raise
        finally:
            await self.shutdown()

    async def _run_polling(self):
        while True:
            try:
                await self.update_index()
            except (ClientError, asyncio.TimeoutError) as exc:
                logger.error("HTTP client error", exc_info=exc)
            await asyncio.sleep(self.update_period)

    async def update_index(self):
        """Download topics and update main index."""
        logger.info("Updating index")
        if is_http_url(self.url):
            path = str(self.cache_dir / "index.md")
            await download_file(self.session, url=self.url, destination=path)
        else:
            path = self.url
        settings.INDEX = Index.from_markdown(path)

    async def shutdown(self):
        if self._session:
            await self._session.close()
            self._session = None


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
    asyncio.run(IndexUpdater().update_index())
    pprint(settings.INDEX)


if __name__ == "__main__":
    main()
