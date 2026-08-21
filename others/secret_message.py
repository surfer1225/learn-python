"""Decode a secret message hidden in a published Google Doc.

Problem
-------
The doc holds a single table with three columns::

    x-coordinate | Character | y-coordinate

Each row places one Unicode character at one (x, y) cell of a 2D grid.
Rendering that grid in a fixed-width font spells out a sequence of uppercase
letters -- the secret message. Coordinates start at 0 and have no upper bound,
and any cell without a specified character is a space.

Orientation
-----------
(0, 0) is the **bottom-left** corner: x grows to the right, y grows *upward*.
So the grid must be printed from the highest y down to 0; printing rows in
ascending y order would render the letters upside down.

Approach
--------
1. Download the published HTML (``.../pub``).
2. Walk it with :mod:`html.parser` from the standard library, collecting the
   text of every table cell. Regexes are avoided because Google's export wraps
   each cell in nested ``<p>``/``<span>`` tags and escapes the block-drawing
   characters as numeric entities (``&#9608;`` -> U+2588); the parser handles
   both for free.
3. Keep only rows that look like data -- exactly three cells whose first and
   third parse as integers. That discards the header row without hardcoding
   its text, and ignores any unrelated table in the document.
4. Store the points in a ``{(x, y): char}`` dict and print row by row.

The dict keeps memory proportional to the number of *specified* characters
rather than to the grid's area, so an arbitrarily large but sparse grid costs
nothing extra. Runtime is linear in the document size plus the printed area.

Usage
-----
As a script (the URL defaults to the full puzzle doc)::

    python secret_message.py [url]

As a module::

    from secret_message import print_secret_message
    print_secret_message("https://docs.google.com/document/d/e/.../pub")

Only the standard library is required. ``certifi`` is used if it happens to be
installed, purely as a fallback for Python builds with no OS trust store.
"""

import ssl
import sys
import urllib.request
from html.parser import HTMLParser

# Default document: the full puzzle doc (the simplified example that draws a
# single 'F' lives at .../2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_...).
DEFAULT_DOC_URL = (
    "https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184"
    "By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub"
)


class _TableParser(HTMLParser):
    """Collect the text of every table cell, grouped by row.

    After ``feed(html)``, ``rows`` is a list of lists of strings: one inner
    list per ``<tr>``, one string per ``<td>``/``<th>`` in it. Nested markup
    inside a cell is flattened, and character references are decoded
    (``convert_charrefs=True``), so a cell rendered as ``&#9608;`` arrives as
    the single character ``"█"``.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows = []
        self._row = None  # cells of the <tr> currently open, else None
        self._cell = None  # text chunks of the <td> currently open, else None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._row = []
        elif tag in ("td", "th") and self._row is not None:
            self._cell = []

    def handle_data(self, data):
        # Text arrives in chunks (one per nested element); buffer them all.
        if self._cell is not None:
            self._cell.append(data)

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._cell is not None:
            self._row.append("".join(self._cell).strip())
            self._cell = None
        elif tag == "tr" and self._row is not None:
            self.rows.append(self._row)
            self._row = None


def _ssl_context():
    """Return the TLS context to fetch with.

    ``None`` means "use urllib's default", which is correct on a normally
    configured machine. Some Python installs (notably python.org builds on
    macOS that never ran *Install Certificates.command*) ship without a usable
    CA bundle and fail with CERTIFICATE_VERIFY_FAILED; if ``certifi`` is
    available we point at its bundle instead. Verification stays on either way.
    """
    try:
        import certifi
    except ImportError:
        return None
    return ssl.create_default_context(cafile=certifi.where())


def _fetch(url):
    """Download `url` and return its body decoded as text."""
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, context=_ssl_context()) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset)


def _parse_points(html):
    """Yield ``(x, y, char)`` triples for every data row in `html`.

    A row qualifies only if it has exactly three cells and its coordinate
    cells parse as integers, which skips the ``x-coordinate / Character /
    y-coordinate`` header as well as any table that is not the data table.
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
            continue  # header row or a non-data table
        if char:
            yield x, y, char[0]


def print_secret_message(url):
    """Fetch the Google Doc at `url` and print the grid of characters it encodes.

    This is the one entry point required by the exercise: it takes a single
    argument -- the URL of the published doc -- and prints the message.
    Unspecified cells are printed as spaces; trailing spaces on each line are
    dropped since they carry no information. An empty document prints nothing.
    """
    grid = {(x, y): char for x, y, char in _parse_points(_fetch(url))}
    if not grid:
        return

    max_x = max(x for x, _ in grid)
    max_y = max(y for _, y in grid)

    # y counts upward from the bottom-left origin, so print the top row first.
    for y in range(max_y, -1, -1):
        line = "".join(grid.get((x, y), " ") for x in range(max_x + 1))
        print(line.rstrip())


if __name__ == "__main__":
    print_secret_message(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DOC_URL)
