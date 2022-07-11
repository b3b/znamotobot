"""Project global settings."""
import logging

from environs import Env

from znamotobot.index import Index

env = Env()
env.read_env()

LOG_LEVEL = env.log_level("LOG_LEVEL", logging.WARNING)

INDEX = Index()
INDEX_URL = env("INDEX_URL", "tests/basic.md")

INLINE_MESSAGE_HEADER = env(
    "INLINE_MESSAGE_HEADER", "🙋‍Information on the topic <b>{title}</b>"
)
INLINE_MESSAGE_REMIND_TEXT = env("INLINE_MESSAGE_REMIND_TEXT", "Remind about 💬")

TELEGRAM_INLINE_CACHE_TIME = env.float("TELEGRAM_INLINE_CACHE_TIME", 120)
TELEGRAM_POLLING_TIMEOUT = env.float("TELEGRAM_POLLING_TIMEOUT", 30)
TELEGRAM_TOKEN = env("TELEGRAM_TOKEN")

INDEX_UPDATE_PERIOD = env.float("INDEX_UPDATE_PERIOD", 600)
INDEX_DOWNLOAD_TIMEOUT = env.float("INDEX_DOWNLOAD_TIMEOUT", 60)
INDEX_CACHE_DIR = env("INDEX_CACHE_DIR", "cache")


SENTRY_ENABLE = env.bool("SENTRY_ENABLE", False)
if SENTRY_ENABLE:
    import sentry_sdk
    from sentry_sdk.integrations.aiohttp import AioHttpIntegration

    sentry_sdk.init(
        dsn=env.str("SENTRY_DSN"),
        integrations=[AioHttpIntegration()],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=0.00001,
    )
