# crawler.py
import arxiv
from datetime import datetime, timezone, timedelta
from collections import defaultdict

def parse_topics(topics_str):
    """
    解析主题配置字符串
    Input example: "missing modality:incomplete multimodal learning;agent:llm"
    Returns: 
        keywords_dict: {主标题: [所有相关关键词]}
        all_keywords: 所有需要搜索的关键词列表
    """
    keywords_dict = {}
    all_keywords = []
    
    topics = topics_str.strip().split(';')
    for topic in topics:
        if ':' in topic:
            keywords = topic.strip().split(':')
            main_keyword = keywords[0].strip()
            all_topic_keywords = [k.strip() for k in keywords]
            keywords_dict[main_keyword] = all_topic_keywords
            all_keywords.extend(all_topic_keywords)
    
    return keywords_dict, all_keywords

def fetch_arxiv_papers(topics_str):
    """
    获取arXiv论文，每个主题的等价词合并为一个查询
    topics_str: 主题配置字符串，格式如 "missing modality:incomplete multimodal learning;agent:llm"
    """
    keywords_dict, _ = parse_topics(topics_str)
    papers_by_topic = defaultdict(list)
    date_threshold = datetime.now(timezone.utc) - timedelta(days=7)
    
    # 对每个主题只执行一次查询
    for main_keyword, related_keywords in keywords_dict.items():
        # 构建 OR 查询
        keyword_queries = [f'ti:"{kw}"' for kw in related_keywords]
        query = ' OR '.join(keyword_queries)
        print(query)
        search = arxiv.Search(
            query=query,
            max_results=50,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        try:
            for result in search.results():
                if result.published.replace(tzinfo=timezone.utc) > date_threshold:
                    paper = {
                        'title': result.title,
                        'authors': [author.name for author in result.authors],
                        'published_date': result.published.strftime('%Y-%m-%d'),
                        'url': result.entry_id,
                        'abstract': result.summary
                    }
                    papers_by_topic[main_keyword].append(paper)
                            
        except Exception as e:
            print(f"Error fetching arXiv papers for topic {main_keyword}: {str(e)}")
            continue
    
    return papers_by_topic

def format_email_content(papers_by_topic):
    """
    格式化邮件内容，按主题分组
    """
    current_date = datetime.now().strftime('%Y-%m-%d')
    content = f"Latest arXiv Papers (Last 7 days until {current_date})\n\n"
    
    if not papers_by_topic:
        content += "No papers found in the last 7 days.\n"
        return content
    
    total_papers = sum(len(papers) for papers in papers_by_topic.values())
    content += f"Total papers found: {total_papers}\n\n"
    
    # 遍历每个主题
    for topic, papers in papers_by_topic.items():
        if not papers:
            continue
            
        content += f"=== {topic.upper()} ({len(papers)} papers) ===\n\n"
        
        # 按发布日期排序
        papers.sort(key=lambda x: x['published_date'], reverse=True)
        
        for paper in papers:
            content += f"Title: {paper['title']}\n"
            content += f"Authors: {', '.join(paper['authors'])}\n"
            content += f"Published Date: {paper['published_date']}\n"
            content += f"URL: {paper['url']}\n"
            content += f"Abstract: {paper['abstract']}\n"
            content += "-" * 80 + "\n\n"
    
    return content
