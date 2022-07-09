import pytest

from znamotobot.parser import Section, parse_document


def test_empty_document_parsed():
    assert not list(parse_document(""))


def test_single_category_document_parsed():
    assert list(parse_document("## Category 1\n* Topic 1")) == [
        Section(title="Category 1", topics=[["Topic 1"]])
    ]


def test_document_parsed():
    with open("tests/basic.md") as f:
        text = f.read()
    assert list(parse_document(text)) == [
        Section(
            title="Category 1",
            topics=[
                ['<a href="https://example.org/1">Topic 1.1</a>', " - Example 1"],
                ['<a href="https://example.org/2">Topic 1.2</a>', " - Example 2"],
            ],
        ),
        Section(
            title="Category 2",
            topics=[
                [
                    '<a href="https://example.org/3">Topic 2.1</a>',
                    " - Example &quot;3&quot; &lt; &#x27;4&#x27;¢",
                ],
                ['<a href="https://example.org/4">Topic 2.2</a>'],
                ['<a href="https://example.org/5">Topic 2.3</a>', " - Example 5"],
                ["https://example.org/6 - Example 6"],
                ["https://example.org/7"],
                ["Topic 2.4"],
                [
                    "https://example.org/8 - ",
                    "<strong>Example</strong>",
                    " ",
                    "<em>8</em>",
                ],
                ["https://example.org/9"],
            ],
        ),
    ]
