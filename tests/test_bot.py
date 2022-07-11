import pytest

from unittest.mock import AsyncMock
from znamotobot.bot import BotRunner, handle_inline_query
from znamotobot.index import Index


@pytest.fixture
def mocked_bot(mocker):
    return mocker.patch("znamotobot.bot.bot", AsyncMock())


@pytest.fixture
def basic_index(mocker):
    mocker.patch("znamotobot.settings.INDEX", Index.from_markdown("tests/basic.md"))


@pytest.mark.asyncio
async def test_query_answered_with_message(mocker, basic_index, mocked_bot):
    mocker.patch("znamotobot.settings.INLINE_MESSAGE_HEADER", "Test message header")
    message_mock = AsyncMock()
    message_mock.query = ""

    await handle_inline_query(inline_query=message_mock)
    mocked_bot.answer_inline_query.assert_called_once()

    first_message_text = mocked_bot.answer_inline_query.call_args_list[0][0][1][0][
        "input_message_content"
    ]["message_text"]
    assert first_message_text.startswith("Test message header")
