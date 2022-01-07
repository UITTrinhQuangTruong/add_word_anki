import bs4
import requests


def get_page_content(url):
    headers = requests.utils.default_headers()

    headers.update(
        {
            "User-Agent": "My User Agent 1.0",
        }
    )

    page = requests.get(url, headers=headers)
    return bs4.BeautifulSoup(page.text, "html.parser")
