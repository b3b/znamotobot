from aioresponses import aioresponses
from aiohttp import ClientSession
import pytest
from znamotobot.updater import download_file, save_content, update_index
from unittest.mock import ANY


@pytest.mark.asyncio
async def test_index_updated_from_url(tmpdir, mocker):
    cache_dir = tmpdir / "cache"
    assert not cache_dir.exists()
    mocker.patch("znamotobot.settings.INDEX_URL", "https://example.org")
    mocker.patch("znamotobot.settings.INDEX_CACHE_DIR", cache_dir)
    from_markdown = mocker.patch("znamotobot.index.Index.from_markdown")
    download_file = mocker.patch("znamotobot.updater.download_file")

    await update_index()

    download_file.assert_called_once()
    from_markdown.assert_called_once()
    assert cache_dir.exists()


@pytest.mark.asyncio
async def test_index_updated_from_file_path(tmpdir, mocker):
    cache_dir = tmpdir / "cache"
    assert not cache_dir.exists()

    mocker.patch("znamotobot.settings.INDEX_URL", "tests/basic.md")
    mocker.patch("znamotobot.settings.INDEX_CACHE_DIR", cache_dir)
    from_markdown = mocker.patch("znamotobot.index.Index.from_markdown")
    download_file = mocker.patch("znamotobot.updater.download_file")

    await update_index()

    download_file.assert_not_called()
    from_markdown.assert_called_once()
    assert not cache_dir.exists()


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
