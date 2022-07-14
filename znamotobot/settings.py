"""Project global settings."""
from environs import Env
from marshmallow.validate import Range

from znamotobot.index import Index

env = Env()
env.read_env()

#: Logging level name, https://docs.python.org/3/library/logging.html#levels
LOG_LEVEL = env.log_level("LOG_LEVEL", "WARNING")

INDEX = Index()

#: Path to the Markdown file to load.
#: Coud be a file path: "lists/list.md",
#: or http/https URL: "http://example.org/list.md"
INDEX_URL = env("INDEX_URL", "tests/basic.md")

#: String to use as a chat message header
INLINE_MESSAGE_HEADER = env(
    "INLINE_MESSAGE_HEADER", "🙋‍Information on the topic <b>{title}</b>"
)

#: String to use as a "remind" button text
INLINE_MESSAGE_REMIND_TEXT = env("INLINE_MESSAGE_REMIND_TEXT", "Remind about 💬")

#: Number of items (sections) to show on the page of the scrollable inline menu.
#: Maximum value is 50: https://core.telegram.org/bots/api#answerinlinequery
INLINE_QUERY_ITEMS_PER_PAGE = env.int(
    "INLINE_QUERY_ITEMS_PER_PAGE", 20, validate=Range(min=0, max=50)
)

#: The maximum amount of time in seconds
#: that the result of the inline query may be cached on the server
TELEGRAM_INLINE_CACHE_TIME = env.float("TELEGRAM_INLINE_CACHE_TIME", 120)

#: AIOgram bot executor `polling_timeout`
TELEGRAM_POLLING_TIMEOUT = env.float("TELEGRAM_POLLING_TIMEOUT", 30)

#: Bot unique authentication token
TELEGRAM_TOKEN = env("TELEGRAM_TOKEN")

#: How often to reread from the `INDEX_URL` location, time in seconds
INDEX_UPDATE_PERIOD = env.float("INDEX_UPDATE_PERIOD", 600)

#: HTTP request to `INDEX_URL` total timeout, in seconds
INDEX_DOWNLOAD_TIMEOUT = env.float("INDEX_DOWNLOAD_TIMEOUT", 60)

#: Local path to directory where to store downloaded Markdown file
INDEX_CACHE_DIR = env("INDEX_CACHE_DIR", "cache")

#: Enable the Sentry service client for events and issues logging
SENTRY_ENABLE = env.bool("SENTRY_ENABLE", False)

if SENTRY_ENABLE:
    import sentry_sdk
    from sentry_sdk.integrations.aiohttp import AioHttpIntegration

    #: DSN where to send events
    SENTRY_DSN = env.str("SENTRY_DSN")

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[AioHttpIntegration()],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=0.00001,
    )
