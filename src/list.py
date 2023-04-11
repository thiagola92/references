def list_contains_one_link_only(bookmarks: list[list | str]):
    """Check if follows the LINK pattern"""
    return len(bookmarks) == 1 and bookmarks[0].startswith("http")
