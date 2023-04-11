import re


def increase_lists_indentations(text: str) -> str:
    return re.sub(r"^( *)-( *)", r"\1  -\2", text, flags=re.MULTILINE)


def headers_to_list(text: str) -> str:
    return re.sub(r"^( *)#( *)", r"\1-\2", text, flags=re.MULTILINE)


def remove_markdown_prefix(line: str) -> str:
    return line.strip().removeprefix("#").removeprefix("-").strip()
