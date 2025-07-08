# services/faissdb.py

import faiss
import numpy as np
import os
import json
from core import settings
from .ai import OpenAIClient
from .db import MySQLClient

class FAISSClient():

    def __init__(self):
        self.index_file_path = settings.FAISS_INDEX_FILE
        self.map_file_path = settings.FAISS_MAP_FILE
        self.dim = settings.OPENAI_EMBEDDING_DIM
        self.ai_client = OpenAIClient()
        self.db_client = MySQLClient()

    def _load_faiss_index(self):
        if os.path.exists(self.index_file_path):
            print(f"FAISS : Loading FAISS Index({self.index_file_path})...", end=" ")
            index = faiss.read_index(self.index_file_path)
            print("OK.")
            return index
        else:
            print("FAISS : Create new FAISS Index...", end=" ")
            index = faiss.IndexFlatL2(self.dim)
            print("OK.")
            return index

    def _load_id_map(self):
        if os.path.exists(self.map_file_path):
            print(f"FAISS : Loading Map file({self.map_file_path})...", end=" ")
            with open(self.map_file_path, "r") as f:
                id_map = json.load(f)
            print("OK.")
            return id_map
        else:
            print("Create new Map file...", end=" ")
            id_map = {}
            print("OK.")
            return id_map
        
    def _save_faiss_index(self, index):
        print(f"FAISS : Saving FAISS Index({self.index_file_path})...", end=" ")
        faiss.write_index(index, self.index_file_path)
        print("OK.")

    def _save_id_map(self, id_map):
        print(f"FAISS : Saving Map file({self.map_file_path})...", end=" ")
        with open(self.map_file_path, "w") as f:
            json.dump(id_map, f, indent=2)
        print("OK.")

    def add(self, papers):
        index = self._load_faiss_index()
        id_map = self._load_id_map()
        existing_ids = set(id_map.values())

        new_vectors = []
        new_arxiv_ids = []

        for paper in papers:
            arxiv_id = paper.arxiv_id
            if arxiv_id in existing_ids:
                continue
            text = paper.title + "\n\n" + paper.abstract
            vec = self.ai_client.get_embedding(text)
            vec = np.array(vec).astype("float32")

            new_vectors.append(vec)
            new_arxiv_ids.append(arxiv_id)

        if not new_vectors:
            print("FAISS : No vectors to add!")
            return
        
        print("FAISS : Trying to add new embeddings...", end=" ")
        index.add(np.vstack(new_vectors))
        print(f"OK, {len(new_vectors)} embeddings added.")

        start_idx = len(id_map)
        for i, arxiv_id in enumerate(new_arxiv_ids):
            id_map[start_idx + i] = arxiv_id

        self._save_faiss_index(index)
        self._save_id_map(id_map)
        self.db_client.update_embedded_papers(new_arxiv_ids)

    def query(self, query, k=5):
        index = self._load_faiss_index()
        id_map = self._load_id_map()
        query_embedding = self.ai_client.get_embedding(query)
        print(f"FAISS : Trying to search {k} embeddings by query...", end=" ")
        D, I = index.search(np.array([query_embedding]).astype("float32"), k=k)
        print(f"OK, {I[0].shape[0]} embeddings found.")

        arxiv_ids = [id_map[str(idx)] for idx in I[0]]
        papers = self.db_client.fetch_papers_by_arxiv_ids(arxiv_ids)

        return papers