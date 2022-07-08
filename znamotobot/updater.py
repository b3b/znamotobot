"""Update topic index."""

import logging

from znamotobot import settings
from znamotobot.index import Index

logger = logging.getLogger(__name__)


async def update_index():
    logger.info("Updating index")
    settings.INDEX = Index.from_markdown(settings.INDEX_URL)
