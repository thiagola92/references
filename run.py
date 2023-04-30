import json
from pathlib import Path

from src.error import raise_error_on_wrong_indentation
from src.html import get_html
from src.markdown import (
    headers_to_list,
    increase_lists_indentations,
    remove_markdown_prefix,
)
from src.text import get_indentation, get_not_empty_lines

INDENTATION = 2

directory = Path("bookmarks")


def read_bookmarks():
    for file in directory.iterdir():
        text = file.read_text()
        text = increase_lists_indentations(text)
        text = headers_to_list(text)
        lines = get_not_empty_lines(text)
        bookmarks, _ = read_indentation(lines)
        filename = file.stem

        Path(f"output/{filename}.json").write_text(json.dumps(bookmarks, indent=2))

        yield bookmarks, filename


def read_indentation(
    lines: list[str], current_indentation: int = 0, i: int = 0
) -> list[list | str, int]:
    """
    LINK: List with one url inside
        ["https://www.google.com"]
    FOLDER: List where the first element is a List[str] and the others can be LINK/FOLDER
        ["Folder name", ["https://google.com"], ["https://facebook.com"], ["https://youtube.com"]]

    returns a List with everything found
        [
            ["First folder", ["https://google.com"], ["https://facebook.com"], ["https://youtube.com"]],
            ["Second folder", ["https://instagram.com"]],
            ["https://www.tiktok.com"]
        ]
    """
    acc = []

    while i < len(lines):
        line = lines[i]
        line_indentation = get_indentation(line)

        raise_error_on_wrong_indentation(
            line_indentation, current_indentation, INDENTATION, line
        )

        if line_indentation > current_indentation:
            a, i = read_indentation(lines, current_indentation + INDENTATION, i)
            acc[-1].extend(a)
        elif line_indentation < current_indentation:
            return acc, i - 1
        else:
            acc.append([remove_markdown_prefix(line)])

        i += 1

    return acc, i


def write_bookmarks():
    html = ""

    for bookmarks, filename in read_bookmarks():
        html += get_html([filename] + bookmarks, 0)

    Path(f"output/bookmarks.html").write_text(html)


write_bookmarks()
