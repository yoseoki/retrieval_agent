# cli/main.py

from .commands import *

arxiv_id = input("Please input arxiv id (ex. 2201.05229v1) : ")
add_specific_paper_to_db(arxiv_id)