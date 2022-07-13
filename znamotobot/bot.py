"""Telegram bot."""
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

from znamotobot import settings
from znamotobot.pagination import Page
from znamotobot.runner import BotRunner

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=(
        "%(asctime)s.%(msecs)03d %(levelname)s %(module)s - "
        "%(funcName)s: %(message)s"
    ),
)
logger = logging.getLogger()

bot = Bot(token=settings.TELEGRAM_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.inline_handler()
async def handle_inline_query(inline_query: InlineQuery):
    logger.debug("Running <handle_inline_query>")
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            settings.INLINE_MESSAGE_REMIND_TEXT,
            switch_inline_query_current_chat="",
        )
    )
    sections = Page(
        items=settings.INDEX.search(inline_query.query),
        limit=settings.INLINE_QUERY_ITEMS_PER_PAGE,
        offset=int(inline_query.offset or 0),
    )
    menu = [
        InlineQueryResultArticle(
            id=str(hash(title)),
            title=title,
            input_message_content=build_topics_content(title, topics),
            hide_url=True,
            reply_markup=keyboard,
        )
        for title, topics in sections
    ]
    await bot.answer_inline_query(
        inline_query.id,
        menu,
        cache_time=settings.TELEGRAM_INLINE_CACHE_TIME,
        next_offset=str(sections.next_offset or ""),
    )


def build_topics_content(title, topics: str) -> InputTextMessageContent:
    header = settings.INLINE_MESSAGE_HEADER.format(title=title)
    return InputTextMessageContent(
        message_text=f"{header}\n\n{topics}",
        disable_web_page_preview=True,
        parse_mode="html",
    )


if __name__ == "__main__":
    BotRunner(dp).start()
