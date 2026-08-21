"""Decode a secret message from a published Google Doc.

The doc contains a 3-column table of (x-coordinate, character, y-coordinate).
Printing the characters at their positions in a fixed-width font reveals a
sequence of uppercase letters.

Usage:
    python secret_message.py [url]
"""

import ssl
import sys
import urllib.request
from html.parser import HTMLParser


class _TableParser(HTMLParser):
    """Collect the cell text of every table row in the document."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows = []
        self._row = None
        self._cell = None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._row = []
        elif tag in ("td", "th") and self._row is not None:
            self._cell = []

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._cell is not None:
            self._row.append("".join(self._cell).strip())
            self._cell = None
        elif tag == "tr" and self._row is not None:
            self.rows.append(self._row)
            self._row = None

    def handle_data(self, data):
        if self._cell is not None:
            self._cell.append(data)


def _fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset)


def _parse_points(html):
    """Yield (x, y, char) triples from the document's table rows.

    Rows whose coordinate cells are not integers (the header row, stray
    tables) are skipped.
    """
    parser = _TableParser()
    parser.feed(html)
    for row in parser.rows:
        if len(row) != 3:
            continue
        x_text, char, y_text = row
        try:
            x, y = int(x_text), int(y_text)
        except ValueError:
            continue
        if char:
            yield x, y, char[0]


def print_secret_message(url):
    """Fetch the Google Doc at `url` and print the grid of characters it encodes."""
    grid = {(x, y): char for x, y, char in _parse_points(_fetch(url))}
    if not grid:
        return

    max_x = max(x for x, _ in grid)
    max_y = max(y for _, y in grid)

    # (0, 0) is the bottom-left corner: x grows right, y grows up, so the
    # highest y is printed first.
    for y in range(max_y, -1, -1):
        line = "".join(grid.get((x, y), " ") for x in range(max_x + 1))
        print(line.rstrip())


if __name__ == "__main__":
    default_url = (
        "https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJS"
        "MAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub"
    )
    print_secret_message(sys.argv[1] if len(sys.argv) > 1 else default_url)
