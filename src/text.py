def get_indentation(line: str) -> int:
    return len(line) - len(line.lstrip())


def indent(text: str, spaces: int) -> str:
    return ("    " * max(spaces, 0)) + text


def is_a_link(obj: list | str) -> bool:
    return isinstance(obj, str) and obj.startswith("http")


def is_a_folder(obj: list | str) -> bool:
    return isinstance(obj, str) and not obj.startswith("http")


def get_not_empty_lines(text: str) -> list[str]:
    lines = text.split("\n")
    lines = [line for line in lines if is_not_empty(line)]
    return lines


def is_not_empty(text: str) -> bool:
    return text.strip() != ""
