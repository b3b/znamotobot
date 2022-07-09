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

TELEGRAM_INLINE_CACHE_TIME = env.float("TELEGRAM_INLINE_CACHE_TIME", 120)
TELEGRAM_POLLING_TIMEOUT = env.float("TELEGRAM_POLLING_TIMEOUT", 30)
TELEGRAM_TOKEN = env("TELEGRAM_TOKEN")

INDEX_DOWNLOAD_TIMEOUT = env.float("INDEX_DOWNLOAD_TIMEOUT", 60)
INDEX_CACHE_DIR = env("INDEX_CACHE_DIR", "cache")
INDEX_MAX_FILE_SIZE = env.int("INDEX_MAX_FILE_SIZE", 1048576)
