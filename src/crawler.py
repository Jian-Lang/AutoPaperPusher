import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import arxiv

def fetch_dblp_papers(keywords):
    all_papers = []
    for keyword in keywords:
        url = f"https://dblp.org/search/publ/api?q={keyword}&format=json"
        response = requests.get(url)
        
        if response.status_code != 200:
            continue
        
        data = response.json()
        hits = data.get('result', {}).get('hits', {}).get('hit', [])
        
        for hit in hits:
            info = hit.get('info', {})
            authors_info = info.get('authors', {}).get('author', [])
            if isinstance(authors_info, dict):
                authors = [authors_info.get('text', '')]
            else:
                authors = [author.get('text', '') for author in authors_info]
                
            paper = {
                'title': info.get('title', ''),
                'authors': authors,
                'venue': info.get('venue', ''),
                'year': info.get('year', ''),
                'url': info.get('url', ''),
                'source': 'DBLP'
            }
            all_papers.append(paper)
    
    return all_papers

def fetch_arxiv_papers(keywords):
    all_papers = []
    # 设置查询时间范围为最近7天
    date_threshold = datetime.now() - timedelta(days=7)
    
    for keyword in keywords:
        # 构建arXiv查询
        search = arxiv.Search(
            query=keyword,
            max_results=50,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        for result in search.results():
            # 检查论文发布时间
            if result.published > date_threshold:
                paper = {
                    'title': result.title,
                    'authors': [author.name for author in result.authors],
                    'venue': 'arXiv',
                    'year': result.published.year,
                    'url': result.entry_id,
                    'source': 'arXiv',
                    'abstract': result.summary
                }
                all_papers.append(paper)
    
    return all_papers

def format_email_content(papers):
    """
    格式化邮件内容，按来源分类展示论文
    """
    content = "Latest papers from DBLP and arXiv:\n\n"
    
    # 按来源分组
    sources = {'DBLP': [], 'arXiv': []}
    for paper in papers:
        sources[paper['source']].append(paper)
    
    # 格式化每个来源的论文
    for source, source_papers in sources.items():
        content += f"=== {source} Papers ===\n\n"
        for paper in source_papers:
            content += f"Title: {paper['title']}\n"
            content += f"Authors: {', '.join(paper['authors'])}\n"
            content += f"Venue: {paper['venue']}\n"
            content += f"Year: {paper['year']}\n"
            content += f"URL: {paper['url']}\n"
            # 如果是arXiv论文，添加摘要
            if source == 'arXiv' and 'abstract' in paper:
                content += f"Abstract: {paper['abstract']}\n"
            content += "-" * 50 + "\n"
        content += "\n"
    
    return content
