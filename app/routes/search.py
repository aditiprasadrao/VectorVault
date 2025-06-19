from flask import Blueprint, request, render_template
from app.models import Document, Query
from app.services import faiss_index, embedder
from app import db
from app.utils.logger import logger
import json

search_bp = Blueprint('search', __name__, url_prefix='/search')

@search_bp.route('/', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        query = request.form['query']
        doc_id = request.form['document_id']
        document = Document.query.get(doc_id)

        query_vector = embedder.embed_query(query)
        res_ids = faiss_index.search_faiss(query_vector, document.vector_path)

        results = [f"Chunk {i}" for i in res_ids]

        q = Query(document_id=doc_id, query_text=query, results=json.dumps(results))
        db.session.add(q)
        db.session.commit()
        logger.info(f"Query: {query}")

    documents = Document.query.all()
    return render_template('search.html', documents=documents, results=results)
