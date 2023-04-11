from src.list import list_contains_one_link_only
from src.text import indent, is_a_folder, is_a_link
from src.website import get_website_title


def get_html(obj: list | str, spaces: int) -> str:
    if is_a_link(obj):
        title = get_website_title(obj)
        return get_html_link(obj, title, spaces)

    if is_a_folder(obj):
        return get_html_folder_start(obj, spaces)

    if list_contains_one_link_only(obj):
        return get_html(obj[0], spaces + 1)

    return get_html_folder_end(obj, spaces + 1)


def get_html_link(link: str, title: str, spaces: int) -> str:
    return indent(f'<DT><A HREF="{link}">{title}</A>\n', spaces)


def get_html_folder_start(name: str, spaces: int) -> str:
    line1 = indent(f"<DT><H3>{name}</H3>\n", spaces)
    line2 = indent("<DL><p>\n", spaces)
    return line1 + line2


def get_html_folder_end(folders: list, spaces: int) -> str:
    content = "".join([get_html(folder, spaces) for folder in folders])
    ending = indent("</DL><p>\n", spaces)
    return content + ending
