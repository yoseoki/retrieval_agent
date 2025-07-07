# cli/commands.py

import services.ai as AI
import services.crawler as CRAWLER
import services.db as DB
import services.faissdb as FDB
import services.notion as NOTION

def add_specific_paper_to_db(arxiv_ids):
    crawler = CRAWLER.ArxivAPIClient()
    dbms = DB.MySQLClient()

    if str(type(arxiv_ids)) == "<class 'str'>": papers = crawler.search_arxiv_with_ids([arxiv_ids])
    else: papers = crawler.search_arxiv_with_ids(arxiv_ids)
    dbms.save_papers(papers)
    print("create over!")

def add_query_paper_to_db(query):
    crawler = CRAWLER.ArxivAPIClient()
    dbms = DB.MySQLClient()

    papers = crawler.search_arxiv_with_query(query)
    dbms.save_papers(papers)
    print("create over!")

def update():
    dbms = DB.MySQLClient()
    faiss_dbms = FDB.FAISSClient()

    papers = dbms.fetch_papers_by_unembed()
    faiss_dbms.add(papers)
    print("update over!")

def translate_specific_paper(arxiv_ids):
    dbms = DB.MySQLClient()
    genai = AI.GenAIClient()
    notion = NOTION.NotionClient()

    if str(type(arxiv_ids)) == "<class 'str'>": papers = dbms.fetch_papers_by_arxiv_ids([arxiv_ids])
    else: papers = dbms.fetch_papers_by_arxiv_ids(arxiv_ids)
    translated_papers = genai.translate_abstract(papers)
    notion.upload(papers, translated_papers)
    print("create over!")

def translate_query_paper(query):
    genai = AI.GenAIClient()
    faiss_dbms = FDB.FAISSClient()
    notion = NOTION.NotionClient()

    papers = faiss_dbms.query(query)
    translated_papers = genai.translate_abstract(papers)
    notion.upload(papers, translated_papers)
    print("create over!")

