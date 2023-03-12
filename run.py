import json
import re
from pathlib import Path
from urllib.parse import urlparse

import requests
from parsel import Selector

directory = Path("bookmarks")


def read_bookmarks():
    for file in directory.iterdir():
        text = file.read_text()
        text = re.sub("^- ", "  - ", text, flags=re.MULTILINE)
        text = re.sub("^# ", "- ", text, flags=re.MULTILINE)
        lines = [l for l in text.split("\n") if l.strip() != ""]
        bookmarks, _ = read_indentation(lines)
        filename = file.stem

        Path(f"output/{filename}.json").write_text(json.dumps(bookmarks, indent=2))

        yield bookmarks, filename


def read_indentation(
    lines: list[str], indentation: int = 0, i: int = 0
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

        if get_indentation(line) > indentation:
            a, i = read_indentation(lines, indentation + 2, i)
            acc[-1].extend(a)
        elif get_indentation(line) < indentation:
            return acc, i - 1
        else:
            acc.append([remove_prefix(line)])

        i += 1

    return acc, i


def get_indentation(line: str) -> int:
    return len(line) - len(line.lstrip())


def remove_prefix(line: str) -> str:
    return line.strip().removeprefix("#").removeprefix("-").strip()


def write_html(bookmarks: list | str, spaces: int) -> str:
    if isinstance(bookmarks, str):
        if bookmarks.startswith("http"):
            return write_html_link(bookmarks, spaces)
        return write_html_folder_start(bookmarks, spaces)

    if contains_one_link(bookmarks):
        return write_html(bookmarks[0], spaces + 1)

    return write_html_folder_end(bookmarks, spaces + 1)


def write_html_link(link: str, spaces: int) -> str:
    title = get_title(link)
    return indent(f'<DT><A HREF="{link}">{title}</A>\n', spaces)


def write_html_folder_start(name: str, spaces: int) -> str:
    line1 = indent(f"<DT><H3>{name}</H3>\n", spaces)
    line2 = indent("<DL><p>\n", spaces)
    return line1 + line2


def write_html_folder_end(folders: list, spaces: int) -> str:
    content = "".join([write_html(f, spaces) for f in folders])
    ending = indent("</DL><p>\n", spaces)
    return content + ending


def contains_one_link(bookmarks: list[list | str]):
    """Check if follows the LINK pattern"""
    return len(bookmarks) == 1 and bookmarks[0].startswith("http")


def indent(text: str, spaces: int) -> str:
    return ("    " * max(spaces, 0)) + text


def get_title(link: str) -> str:
    print(link)
    response = requests.get(link)

    try:
        return (
            Selector(text=response.text)
            .xpath("//title/text()")
            .get(urlparse(link).hostname)
        )
    except Exception as e:
        print(e)

    return urlparse(link).hostname


def write_bookmarks():
    html = ""

    for bookmarks, filename in read_bookmarks():
        html += write_html([filename] + bookmarks, 0)

    Path(f"output/bookmarks.html").write_text(html)


write_bookmarks()
