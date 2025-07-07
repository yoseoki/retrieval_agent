# core/models.py
from dataclasses import dataclass

@dataclass
class Paper:
    arxiv_id: str
    title: str
    abstract: str
    authors : str
    url : str
    published: str
    added_at: str

@dataclass
class NotionArticleRow:
    arxiv_id: str
    title: str
    abstract_en: str
    abstract_ko: str
    url : str