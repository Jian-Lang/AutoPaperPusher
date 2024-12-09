import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json


def fetch_dblp_papers(keyword):
    url = f"https://dblp.org/search/publ/api?q={keyword}&format=json"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()
    hits = data.get('result', {}).get('hits', {}).get('hit', [])

    papers = []
    for hit in hits:
        info = hit.get('info', {})
        paper = {
            'title': info.get('title', ''),
            'authors': info.get('authors', {}).get('author', []),
            'venue': info.get('venue', ''),
            'year': info.get('year', ''),
            'url': info.get('url', '')
        }
        papers.append(paper)

    return papers


def format_email_content(papers):
    content = "Today's latest papers:\n\n"
    for paper in papers:
        content += f"Title: {paper['title']}\n"
        content += f"Authors: {', '.join(paper['authors']) if isinstance(paper['authors'], list) else paper['authors']}\n"
        content += f"Venue: {paper['venue']}\n"
        content += f"Year: {paper['year']}\n"
        content += f"URL: {paper['url']}\n"
        content += "-" * 50 + "\n"
    return content