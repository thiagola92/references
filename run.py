from pathlib import Path

directory = Path("bookmarks")


def read_files():
    for file in directory.iterdir():
        text = file.read_text().replace("- ", "  - ").replace("#", "-")
        lines = [l for l in text.split("\n") if l.strip() != ""]
        acc, _ = read_indentation(lines)
        yield acc


def read_indentation(
    lines: list[str], indentation: int = 0, i: int = 0
) -> list[list | str, int]:
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


def is_link(line: str) -> bool:
    return "- http" in line


def remove_prefix(line: str) -> str:
    return line.strip().removeprefix("#").removeprefix("-").strip()


for f in read_files():
    print(f)
