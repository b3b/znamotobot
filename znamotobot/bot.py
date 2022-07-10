"""Telegram bot."""
import asyncio
import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from znamotobot import settings
from znamotobot.updater import update_index

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
    menu = [
        InlineQueryResultArticle(
            id=str(hash(title)),
            title=title,
            input_message_content=build_topics_content(title, topics),
            hide_url=True,
            reply_markup=keyboard,
        )
        for title, topics in settings.INDEX.search(inline_query.query)
    ]
    await bot.answer_inline_query(
        inline_query.id,
        menu,
        cache_time=settings.TELEGRAM_INLINE_CACHE_TIME,
    )


def build_topics_content(title, topics: str) -> InputTextMessageContent:
    header = settings.INLINE_MESSAGE_HEADER.format(title=title)
    return InputTextMessageContent(
        message_text=f"{header}\n\n{topics}",
        disable_web_page_preview=True,
        parse_mode="html",
    )


def main():
    asyncio.run(update_index())
    asyncio.set_event_loop(asyncio.new_event_loop())
    executor.start_polling(
        dp, skip_updates=True, timeout=settings.TELEGRAM_POLLING_TIMEOUT
    )


if __name__ == "__main__":
    main()
