"""Control bot execution."""
import asyncio

from aiogram import Dispatcher, executor

from znamotobot import settings
from znamotobot.updater import IndexUpdater


class BotRunner:
    """Class to control the execution of the bot and background tasks."""

    def __init__(self, dispatcher: Dispatcher):
        self.dispatcher = dispatcher
        self.updater = IndexUpdater()
        self.tasks: list[asyncio.Task] = []
        self.polling_timeout = settings.TELEGRAM_POLLING_TIMEOUT

    def start(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        executor.start_polling(
            self.dispatcher,
            skip_updates=True,
            timeout=self.polling_timeout,
            on_startup=self.on_startup,
            on_shutdown=self.on_shutdown,
        )

    async def on_startup(
        self, dispatcher: Dispatcher
    ):  # pylint: disable=unused-argument
        self.tasks.append(asyncio.create_task(self.updater.start()))

    async def on_shutdown(
        self, dispatcher: Dispatcher
    ):  # pylint: disable=unused-argument
        for task in self.tasks:
            task.cancel()
