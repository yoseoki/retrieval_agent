import mysql.connector
from core import settings
from core.models import Paper

class MySQLClient():

    def __init__(self):
        self.config = {
            'host': settings.MYSQL_HOST,
            'user': settings.MYSQL_USER,
            'password': settings.MYSQL_PASSWORD,
            'database': settings.MYSQL_DB,
            'charset': 'utf8mb4'
        }

    def save_papers(self, papers):
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor()
        for p in papers:
            try:
                cursor.execute('''
                    INSERT IGNORE INTO papers (arxiv_id, title, abstract, authors, url, published, added_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', (
                    p.arxiv_id,
                    p.title,
                    p.abstract,
                    p.authors,
                    p.url,
                    p.published,
                    p.added_at
                ))
            except Exception as e:
                print(f"Error inserting paper {p.arxiv_id}: {e}")
        conn.commit()
        cursor.close()
        conn.close()

    def fetch_papers_by_unembed(self, limit=1000):
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT arxiv_id, title, abstract, url FROM papers
                WHERE embedded = FALSE
                LIMIT %s
            """, (limit,))
        except Exception as e:
                print(f"Error fetching paper: {e}")
        rows = cursor.fetchall()
        results = []
        for row in rows:
            result = Paper(
                row['arxiv_id'],
                row['title'],
                row['abstract'],
                "",
                row['url'],
                "",
                ""
            )
            results.append(result)
        cursor.close()
        conn.close()
        return results

    def fetch_papers_by_arxiv_ids(self, arxiv_ids):
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor(dictionary=True)
        placeholders = ', '.join(['%s'] * len(arxiv_ids))  # safe parameter binding
        query = f"SELECT arxiv_id, title, abstract, url FROM papers WHERE arxiv_id IN ({placeholders})"
        try:
            cursor.execute(query, arxiv_ids)
        except Exception as e:
                print(f"Error updating paper: {e}")
        rows = cursor.fetchall()
        results = []
        for row in rows:
            result = Paper(
                row['arxiv_id'],
                row['title'],
                row['abstract'],
                "",
                row['url'],
                "",
                ""
            )
            results.append(result)
        cursor.close()
        conn.close()
        return results
    
    def update_embedded_papers(self, arxiv_ids):
        if not arxiv_ids:
            return
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor()
        placeholders = ', '.join(['%s'] * len(arxiv_ids))
        query = f"UPDATE papers SET embedded = TRUE WHERE arxiv_id IN ({placeholders})"
        try:
            cursor.execute(query, arxiv_ids)
        except Exception as e:
                print(f"Error updating paper: {e}")
        conn.commit()
        cursor.close()
        conn.close()