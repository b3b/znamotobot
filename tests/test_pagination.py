import pytest
from znamotobot.pagination import Page


@pytest.mark.parametrize(
    "limit,offset,expected_content,expected_next_offset",
    (
        [2, 0, ["a", "b"], 2],
        [2, 2, ["c", "d"], 4],
        [2, 4, ["e"], None],
        [100, 0, ["a", "b", "c", "d", "e"], None],
        [0, 0, [], 0],
        [100, 100, [], None],
    ),
)
def test_page_initialized(limit, offset, expected_content, expected_next_offset):
    page = Page(items="abcde", limit=limit, offset=offset)
    assert list(page) == expected_content
    assert page.next_offset == expected_next_offset
