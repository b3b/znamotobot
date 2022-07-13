"""Pagination utils."""
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Page:
    """Limit `items` iterable to `limit` items, starting from a given `offset`.
    >>> list(Page(items="abcde", limit=3, offset=1))
    ['b', 'c', 'd']
    >>> Page(items="abcde", limit=3, offset=1).next_offset
    4
    """

    items: Iterable
    limit: int
    offset: int = 0
    #: Calculated offset for the next page
    next_offset: Optional[int] = field(init=False)

    def __post_init__(self):
        next_offset = self.offset + self.limit
        self.next_offset = next_offset if next_offset < len(self.items) else None

    def __iter__(self):
        return iter(self.items[self.offset : (self.offset + self.limit)])
