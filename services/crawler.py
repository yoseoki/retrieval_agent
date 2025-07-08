# services/crawler.py

import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from core import settings
from core.models import Paper


class ArxivAPIClient():
    
    def __init__(self):
        self.base_url = settings.SOURCE_API_BASE_URL

    def _parse_entries(self, xml_content):
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        root = ET.fromstring(xml_content)
        papers = []
        for entry in root.findall('atom:entry', ns):
            paper = Paper(
                entry.find('atom:id', ns).text.split('/')[-1],
                entry.find('atom:title', ns).text.strip().replace('\n', ' '),
                entry.find('atom:summary', ns).text.strip().replace('\n', ' '),
                ', '.join([a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)]),
                entry.find('atom:id', ns).text,
                entry.find('atom:published', ns).text,
                datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            )
            papers.append(paper)
        return papers
    
    def search_arxiv_with_query(self, query, max_results=30):
        print("CRAWL : Trying to crawl papers by query...", end=" ")
        params = {
            "search_query": query,
            "start": 0,
            "max_results": max_results,
            "sortBy": "relevance",
            "sortOrder": "descending"
        }
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        papers = self._parse_entries(response.text)
        print(f"OK, {len(papers)} papers found.")
        return papers
    
    def search_arxiv_with_ids(self, arxiv_ids):
        print(f"CRAWL : Trying to crawl {len(arxiv_ids)} papers...", end=" ")
        id_list_str = ",".join(arxiv_ids)
        params = {
            "id_list": id_list_str
        }
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        papers = self._parse_entries(response.text)
        print(f"OK, {len(papers)} papers found.")
        return papers