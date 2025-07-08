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

    def _get_existing_arxiv_ids(self):
        url = f"{self.query_url}/{self.database_id}/query"
        arxiv_ids = []
        has_more = True
        next_cursor = None

        while has_more:
            payload = {}
            if next_cursor:
                payload["start_cursor"] = next_cursor

            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()

            for result in data["results"]:
                properties = result.get("properties", {})
                id_field = properties.get("ID", {})
                if "title" in id_field and id_field["title"]:
                    arxiv_id = id_field["title"][0]["text"]["content"]
                    arxiv_ids.append(arxiv_id)

            has_more = data.get("has_more", False)
            next_cursor = data.get("next_cursor")

        return arxiv_ids

    def _build_rows(self, papers, translated_papers):
        existing_ids = set(self._get_existing_arxiv_ids())
        rows = []
        for p, new_p in zip(papers, translated_papers):
            if p.arxiv_id in existing_ids: continue
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
        print(f"Notion : Trying to upload {len(papers)} papers...", end=" ")
        rows = self._build_rows(papers, translated_papers)
        for row in rows:
            self._upload_row(row)
        print(f"OK, {len(rows)} papers uploaded.")