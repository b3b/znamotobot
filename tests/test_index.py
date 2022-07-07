import pytest

from znamotobot.index import Index


@pytest.fixture
def index_2_entries():
    return Index([["e0", "e0 text"], ["entry 1", "entry 1 text"]])


def test_empty_index_created():
    assert not len(Index())


def test_index_created_with_entries(index_2_entries):
    assert len(index_2_entries) == 2


def test_index_loaded_from_md_file(mocker):
    parse_document = mocker.patch(
        "znamotobot.index.parse_document",
        return_value=[
            ("Category 1", [["Topic 1"], ["Topic 2"]]),
        ],
    )

    obj = Index.from_markdown("tests/basic.md")

    assert obj == Index([("Category 1", "✴ Topic 1\n\n✴ Topic 2")])
    parse_document.assert_called_once()
    assert "# Example" in parse_document.call_args[0][0]
