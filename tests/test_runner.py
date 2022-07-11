from unittest.mock import AsyncMock
import pytest
from znamotobot.bot import dp
from znamotobot.runner import BotRunner


@pytest.mark.asyncio
async def test_tasks_started(mocker):
    runner = BotRunner(dp)
    start_polling = mocker.patch("aiogram.executor.start_polling")
    start_updater = mocker.patch("znamotobot.updater.IndexUpdater.start", AsyncMock())

    runner.start()

    await runner.on_startup(runner.dispatcher)
    await runner.on_shutdown(runner.dispatcher)

    start_polling.assert_called_once()
    start_updater.assert_called_once()
