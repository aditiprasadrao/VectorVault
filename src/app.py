from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
import yaml
from pdf_processor.extract import extract_text
from faiss_index.faiss_handler import embed_and_add_to_index, search_query
from database.db import store_pdf_metadata, store_query_result
from utils.logger import setup_logger
from utils.helpers import chunk_text

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

UPLOAD_FOLDER = config["app"]["upload_folder"]
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

logger = setup_logger()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

chunks = []

@app.route("/", methods=["GET", "POST"])
def index():
    global chunks
    if request.method == "POST":
        file = request.files["pdf"]
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            text = extract_text(file_path)
            chunks = chunk_text(text)
            embed_and_add_to_index(chunks)
            pdf_id = store_pdf_metadata(filename)
            logger.info(f"PDF '{filename}' uploaded and embedded.")
            return render_template("index.html", msg="PDF Uploaded", pdf_id=pdf_id)
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def query():
    user_query = request.form["query"]
    pdf_id = int(request.form["pdf_id"])
    results = search_query(user_query, chunks)
    result_text = "\n\n".join(results)
    store_query_result(pdf_id, user_query, result_text)
    logger.info(f"Query '{user_query}' processed.")
    return render_template("index.html", msg="Results", results=results, pdf_id=pdf_id)

if __name__ == "__main__":
    app.run(debug=True)
