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
        # 处理作者信息：从字典中提取作者名字
        authors_info = info.get('authors', {}).get('author', [])
        if isinstance(authors_info, dict):
            authors = [authors_info.get('text', '')]
        else:
            authors = [author.get('text', '') for author in authors_info]
            
        paper = {
            'title': info.get('title', ''),
            'authors': authors,  # 现在authors是字符串列表
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
        # 现在authors是字符串列表，可以直接join
        content += f"Authors: {', '.join(paper['authors'])}\n"
        content += f"Venue: {paper['venue']}\n"
        content += f"Year: {paper['year']}\n"
        content += f"URL: {paper['url']}\n"
        content += "-" * 50 + "\n"
    return content
