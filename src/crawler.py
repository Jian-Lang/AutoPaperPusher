import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import arxiv
from datetime import timezone

def fetch_dblp_papers(keywords):
    """
    获取DBLP论文，支持多个关键词，并筛选最近7天的论文
    """
    all_papers = []
    # 设置时间阈值
    date_threshold = datetime.now() - timedelta(days=7)
    
    for keyword in keywords:
        url = f"https://dblp.org/search/publ/api?q={keyword}&format=json"
        response = requests.get(url)
        
        if response.status_code != 200:
            continue
        
        data = response.json()
        hits = data.get('result', {}).get('hits', {}).get('hit', [])
        
        for hit in hits:
            info = hit.get('info', {})
            # 获取论文日期
            try:
                paper_date = datetime.strptime(info.get('year', ''), '%Y')
                # 如果是今年的论文则保留
                if paper_date.year == datetime.now().year:
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
            except ValueError:
                continue
    
    return all_papers

def fetch_arxiv_papers(keywords):
    """
    获取arXiv论文，支持多个关键词
    """
    all_papers = []
    # 设置查询时间范围为最近7天，使用UTC时区
    date_threshold = datetime.now(timezone.utc) - timedelta(days=1)
    
    for keyword in keywords:
        # 构建arXiv查询
        title_query = f'ti:"{keyword}"'  # 使用ti:前缀限制在标题搜索
        search = arxiv.Search(
            query=title_query,
            max_results=50,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        for result in search.results():
            # 确保比较时使用相同的时区
            if result.published.replace(tzinfo=timezone.utc) > date_threshold:
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
    current_date = datetime.now().strftime('%Y-%m-%d')
    content = f"Latest papers from DBLP and arXiv (Last 7 days until {current_date}):\n\n"
    
    # 按来源分组
    sources = {'DBLP': [], 'arXiv': []}
    for paper in papers:
        sources[paper['source']].append(paper)
    
    # 格式化每个来源的论文
    for source, source_papers in sources.items():
        if source_papers:  # 只有当有论文时才显示分类
            content += f"=== {source} Papers ({len(source_papers)} papers) ===\n\n"
            for paper in source_papers:
                content += f"Title: {paper['title']}\n"
                content += f"Authors: {', '.join(paper['authors'])}\n"
                content += f"Venue: {paper['venue']}\n"
                content += f"Year: {paper['year']}\n"
                content += f"URL: {paper['url']}\n"
                if source == 'arXiv' and 'abstract' in paper:
                    content += f"Abstract: {paper['abstract'][:500]}... (truncated)\n"  # 限制摘要长度
                content += "-" * 50 + "\n\n"
        else:
            content += f"=== {source} Papers (No papers found) ===\n\n"
    
    return content
