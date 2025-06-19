from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Document
from app import db
from app.services import pdf_reader, chunker, embedder, faiss_index, nlp_tags
from app.utils.logger import logger
import os, uuid

upload_bp = Blueprint('upload', __name__, url_prefix='/')

@upload_bp.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        save_path = os.path.join('data/uploads', filename)
        file.save(save_path)

        text = pdf_reader.extract_text_from_pdf(save_path)
        chunks = chunker.chunk_text(text)
        vectors = embedder.embed_chunks(chunks)
        
        doc_id = str(uuid.uuid4())
        vector_path = f"data/faiss/{doc_id}.index"
        faiss_index.save_to_faiss(vectors, vector_path)

        tags = nlp_tags.extract_tags(text)

        new_doc = Document(
            name=filename,
            path=save_path,
            vector_path=vector_path,
            nlp_entities=str(tags['entities']),
            topics=str(tags['topics']),
            sentiment=tags['sentiment'],
            summary=tags['summary']
        )
        db.session.add(new_doc)
        db.session.commit()
        logger.info(f"Uploaded and processed: {filename}")
        return redirect(url_for('upload.upload_file'))

    documents = Document.query.all()
    return render_template('upload.html', documents=documents)
