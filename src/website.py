from urllib.parse import urlparse

import requests
from parsel import Selector
from requests import Response


def get_website_title(link: str) -> str:
    print(link)

    try:
        response: Response = requests.get(link)
        response.raise_for_status()

        return (
            Selector(text=response.text)
            .xpath("//title/text()")
            .get(urlparse(link).hostname)
            .replace("\n", " ")
        )
    except Exception as e:
        print(e)

    return urlparse(link).hostname
