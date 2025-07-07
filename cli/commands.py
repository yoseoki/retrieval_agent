# cli/commands.py

import services.ai as AI
import services.crawler as CRAWLER
import services.db as DB
import services.faissdb as FDB

def add_specific_paper_to_db():
    crawler = CRAWLER.ArxivAPIClient()
    dbms = DB.MySQLClient()

    arxiv_id = input("Please input arxiv_id for update db(ex. 2407.04307v1) : ")
    papers = crawler.search_arxiv_with_id(arxiv_id)
    dbms.save_papers(papers)