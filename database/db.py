import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB")
    )

def store_pdf_metadata(name: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pdfs (name) VALUES (%s)", (name,))
    conn.commit()
    pdf_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return pdf_id

def store_query_result(pdf_id: int, query: str, result: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO queries (pdf_id, query, result) VALUES (%s, %s, %s)",
        (pdf_id, query, result)
    )
    conn.commit()
    cursor.close()
    conn.close()
