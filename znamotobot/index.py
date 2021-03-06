"""Storing and searching topics."""
import re
import sys
from collections import OrderedDict
from pprint import pprint

from znamotobot.formatter import format_topics
from znamotobot.parser import parse_document


class Index(OrderedDict):
    """Dictionary of topics."""

    @classmethod
    def from_markdown(cls, path: str) -> "Index":
        """Load topics from the given file path."""
        with open(path, encoding="utf-8") as f:
            return cls(
                [
                    (title, format_topics(topics))
                    for title, topics in parse_document(f.read())
                ]
            )

    def search(self, text: str = "") -> list[tuple[str, str]]:
        """Find topics sections that has `text` in title."""
        return [
            (title, topics)
            for title, topics in self.items()
            if (not text) or re.search(text, title, re.IGNORECASE)
        ]


def main():
    try:
        path = sys.argv[1]
    except IndexError:
        path = "tests/basic.md"
    pprint(Index.from_markdown(path))


if __name__ == "__main__":
    main()
