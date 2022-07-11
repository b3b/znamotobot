import asyncio
from aioresponses import aioresponses

import aiohttp
from aiohttp import ClientSession
import pytest
from unittest.mock import AsyncMock
from znamotobot.updater import (
    IndexUpdater,
    download_file,
    save_content,
)
from unittest.mock import ANY


@pytest.mark.asyncio
async def test_index_updated_from_url(tmpdir, mocker):
    cache_dir = tmpdir / "cache"
    assert not cache_dir.exists()

    mocker.patch("znamotobot.settings.INDEX_URL", "https://example.org")
    mocker.patch("znamotobot.settings.INDEX_CACHE_DIR", cache_dir)
    from_markdown = mocker.patch("znamotobot.index.Index.from_markdown")
    download_file = mocker.patch("znamotobot.updater.download_file")

    updater = IndexUpdater()
    await updater.update_index()

    download_file.assert_called_once()
    from_markdown.assert_called_once()
    assert cache_dir.exists()

    await updater.shutdown()


@pytest.mark.asyncio
async def test_index_updated_from_file_path(tmpdir, mocker):
    cache_dir = tmpdir / "cache"
    assert not cache_dir.exists()

    mocker.patch("znamotobot.settings.INDEX_URL", "tests/basic.md")
    mocker.patch("znamotobot.settings.INDEX_CACHE_DIR", cache_dir)
    from_markdown = mocker.patch("znamotobot.index.Index.from_markdown")
    download_file = mocker.patch("znamotobot.updater.download_file")

    updater = IndexUpdater()
    await updater.update_index()

    download_file.assert_not_called()
    from_markdown.assert_called_once()
    assert cache_dir.exists()

    await updater.shutdown()


@pytest.mark.asyncio
async def test_file_download(mocker):
    save_content = mocker.patch("znamotobot.updater.save_content")
    session = ClientSession()
    with aioresponses() as responses:
        responses.get("https://example.org", body="test download")
        await download_file(session, "https://example.org", "/tmp/index.md")
    save_content.assert_called_once_with(b"test download", "/tmp/index.md")
    await session.close()


@pytest.mark.asyncio
async def test_content_saved(tmpdir):
    path = tmpdir / "test.md"
    await save_content(b"test", path)
    with path.open() as f:
        assert f.read() == "test"


@pytest.mark.asyncio
async def test_exceptions_handled(mocker):
    mocker.patch("asyncio.sleep")
    error_logger = mocker.patch("znamotobot.updater.logger.error")
    invalid_url = aiohttp.client_exceptions.InvalidURL(...)

    update_index = mocker.patch(
        "znamotobot.updater.IndexUpdater.update_index",
        AsyncMock(
            side_effect=[
                invalid_url,
                asyncio.CancelledError(),
            ]
        ),
    )

    updater = IndexUpdater()
    await updater.start()

    assert update_index.call_count == 2
    error_logger.assert_called_once_with("HTTP client error", exc_info=invalid_url)


@pytest.mark.asyncio
async def test_content_not_changed(mocker):
    save_content = mocker.patch("znamotobot.updater.save_content")
    session = ClientSession()

    with aioresponses() as responses:
        responses.get(
            "https://example.org",
            status=301,
        )

        new_etag = await download_file(
            session, "https://example.org", "/tmp/index.md", etag="2128506"
        )
        await session.close()

        headers = list(responses.requests.values())[0][0].kwargs["headers"]
        assert headers["If-None-Match"] == "2128506"
        assert new_etag == "2128506"
        save_content.assert_not_called()
