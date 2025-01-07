# crawler.py
import arxiv
from datetime import datetime, timezone, timedelta
from collections import defaultdict

def parse_topics(topics_str):
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

    keywords_dict, _ = parse_topics(topics_str)
    papers_by_topic = defaultdict(list)
    tz_cn = timezone(timedelta(hours=8))

    date_threshold = (datetime.now(tz_cn) - timedelta(days=2))
    for main_keyword, related_keywords in keywords_dict.items():
        keyword_queries = [f'ti:"{kw}"' for kw in related_keywords]
        query = ' OR '.join(keyword_queries)
        
        search = arxiv.Search(
            query=query,
            max_results=50,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        try:
            for result in search.results():
                paper_time = result.published.replace(tzinfo=timezone.utc).astimezone(tz_cn)
                if paper_time > date_threshold:
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
    current_date = datetime.now().strftime('%Y-%m-%d')
    content = f"Latest arXiv Papers (Last day until {current_date})\n\n"
    
    if not papers_by_topic:
        content += "No papers found in the last day.\n"
        return content
    
    total_papers = sum(len(papers) for papers in papers_by_topic.values())
    content += f"Total papers found: {total_papers}\n\n"
    
    for topic, papers in papers_by_topic.items():
        if not papers:
            continue
            
        content += f"=== {topic.upper()} ({len(papers)} papers) ===\n\n"

        papers.sort(key=lambda x: x['published_date'], reverse=True)
        
        for paper in papers:
            content += f"Title: {paper['title']}\n"
            content += f"Authors: {', '.join(paper['authors'])}\n"
            content += f"Published Date: {paper['published_date']}\n"
            content += f"URL: {paper['url']}\n"
            content += f"Abstract: {paper['abstract']}\n"
            content += "-" * 80 + "\n\n"
    
    return content
