# cli/commands.py

import services.ai as AI
import services.crawler as CRAWLER
import services.db as DB
import services.faissdb as FDB
import services.notion as NOTION

def add_specific_paper_to_db():
    crawler = CRAWLER.ArxivAPIClient()
    dbms = DB.MySQLClient()

    arxiv_id = input("Please input arxiv_id for update db(ex. 2407.04307v1) : ")
    papers = crawler.search_arxiv_with_id(arxiv_id)
    dbms.save_papers(papers)
    print("create over!")

def add_query_paper_to_db():
    crawler = CRAWLER.ArxivAPIClient()
    dbms = DB.MySQLClient()

    query = input("Please input keywords for update db(ex. grassmann manifold learning) : ")
    papers = crawler.search_arxiv_with_query(query)
    dbms.save_papers(papers)
    print("create over!")

def update():
    dbms = DB.MySQLClient()
    faiss_dbms = FDB.FAISSClient()

    papers = dbms.fetch_papers_by_unembed()
    faiss_dbms.add(papers)
    print("update over!")

def translate_specific_paper():
    dbms = DB.MySQLClient()
    genai = AI.GenAIClient()
    notion = NOTION.NotionClient()

    arxiv_id = input("Please input arxiv_id for translate(ex. 2407.04307v1) : ")
    papers = dbms.fetch_papers_by_arxiv_ids([arxiv_id])
    translated_papers = genai.translate_abstract(papers)
    notion.upload(papers, translated_papers)
    print("create over!")

def translate_query_paper():
    genai = AI.GenAIClient()
    faiss_dbms = FDB.FAISSClient()
    notion = NOTION.NotionClient()

    query = input("Please input keywords for query FAISS db(ex. grassmann manifold learning) : ")
    papers = faiss_dbms.query(query)
    translated_papers = genai.translate_abstract(papers)
    notion.upload(papers, translated_papers)
    print("create over!")

