import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime


def fetch_embedded_python_links():
    url = "https://www.python.org/downloads/windows/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    embedded_links = []
    for link in soup.find_all("a"):
        href = link.get("href", "")
        if "embed" in href.lower() and href.endswith(".zip"):
            version = href.split("/")[-2]
            embedded_links.append(
                {
                    "version": version,
                    "url": f"https://www.python.org{href}"
                    if href.startswith("/")
                    else href,
                }
            )

    return embedded_links


def generate_html(links):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Python Embedded Downloads</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .download-list { list-style: none; }
            .download-item { margin: 10px 0; padding: 10px; border: 1px solid #ddd; }
        </style>
    </head>
    <body>
        <h1>Python Embedded Downloads</h1>
        <p>Last updated: {}</p>
        <ul class="download-list">
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"))

    for link in sorted(links, key=lambda x: x["version"], reverse=True):
        html += f"""
            <li class="download-item">
                <strong>Version {link["version"]}</strong><br>
                <a href="{link["url"]}">Download</a>
            </li>
        """

    html += """
        </ul>
    </body>
    </html>
    """

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    links = fetch_embedded_python_links()
    generate_html(links)
