# services/notion.py

import requests
from core import settings
from core.models import NotionArticleRow

class NotionClient():

    def __init__(self):
        self.token = settings.NOTION_API_KEY
        self.database_id = settings.NOTION_DATABASE_ID
        self.page_url = settings.NOTION_PAGE_URL
        self.query_url = settings.NOTION_QUERY_URL
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    def _build_rows(self, papers, translated_papers):
        rows = []
        for p, new_p in zip(papers, translated_papers):
            row = NotionArticleRow(
                p.arxiv_id,
                p.title,
                p.abstract,
                new_p.abstract,
                p.url
            )
            rows.append(row)
        return rows

    def _upload_row(self, row: NotionArticleRow):
        # row: arxiv_id, title, abstract_en, abstract_ko, url
        payload = {
            "parent": { "database_id": self.database_id },
            "properties": {
                "ID": {
                    "title": [{
                        "text": {
                            "content": row.arxiv_id[:2000]  # Notion constraint
                        }
                    }]
                },
                "Title": {
                    "rich_text": [{
                        "text": {
                            "content": row.title[:2000]
                        }
                    }]
                },
                "Abstract_en": {
                    "rich_text": [{
                        "text": {
                            "content": row.abstract_en
                        }
                    }]
                },
                "Abstract_ko": {
                    "rich_text": [{
                        "text": {
                            "content": row.abstract_ko
                        }
                    }]
                },
                "URL": {
                    "url": row.url
                }
            }
        }

        response = requests.post(self.page_url, headers=self.headers, json=payload)
        response.raise_for_status()

    def upload(self, papers, translated_papers):
        rows = self._build_rows(papers, translated_papers)
        for row in rows:
            self._upload_row(row)