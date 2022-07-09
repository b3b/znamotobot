"""Parse markdown lists of topics."""
import html
import re
import sys
from collections.abc import Iterator
from pprint import pprint
from typing import NamedTuple

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from markdown import markdown


class Section(NamedTuple):
    """Topics section."""

    title: str
    topics: list[list[str]]


def parse_document(text: str) -> Iterator[Section]:
    """Generator that yields topics from the given markdown text."""
    soup = BeautifulSoup(markdown(text), "html.parser")
    for section in soup.find_all("h2"):
        topics = list(parse_section(section))
        if topics:
            yield Section(section.text, topics)


def parse_section(section: Tag) -> Iterator[list[str]]:
    for sib in section.find_next_siblings():
        match sib.name:
            case "ul":
                yield from parse_topic_list(sib)
            case "h2":
                break


def parse_topic_list(topic_list: Tag) -> Iterator[list[str]]:
    for topic in topic_list.find_all("li", recursive=False):
        sublist = topic.find("ul")
        if sublist:
            yield from parse_topic_list(sublist)
        else:
            yield list(parse_topic(topic))


def parse_topic(topic: Tag) -> Iterator[str]:
    for elem in topic.children:
        match elem.name:
            case "a" | "em" | "span" | "strong":
                yield str(elem)
            case _:
                yield html.escape(elem.text)


def main():
    try:
        path = sys.argv[1]
    except IndexError:
        path = "tests/basic.md"
    if re.match("^http[s]?://", path):
        text = requests.get(path).text
    else:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    for topic, description in parse_document(text):
        print(topic)
        pprint(description)


if __name__ == "__main__":
    main()
