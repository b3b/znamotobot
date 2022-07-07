"""Topics formatting functions."""


def format_topics(topics: list[list[str]]) -> str:
    """Return string representation for given list of topics."""
    return "\n\n".join([format_topic(items) for items in topics])


def format_topic(items: list[str]) -> str:
    return "✴ " + " ".join(items)
