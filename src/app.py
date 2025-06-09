from pathlib import Path
from dotenv import load_dotenv
env_path = Path(__file__).resolve().parent.parent / '.env'  
load_dotenv(dotenv_path=env_path)

import os


# Now imports that use env vars
from database.db import get_connection
import yaml
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

# Local imports
from pdf_processor.extract import extract_text
from faiss_index.faiss_handler import embed_and_add_to_index, search_query
from database.db import store_pdf_metadata, store_query_result
from utils.logger import setup_logger
from utils.helpers import chunk_text

# --- Setup paths ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, '..', 'templates')
STATIC_DIR = os.path.join(BASE_DIR, '..', 'static')

# --- Initialize app ---
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

# --- Load config ---
with open(os.path.join(BASE_DIR, "..", "config.yaml"), "r") as f:
    config = yaml.safe_load(f)

UPLOAD_FOLDER = config["app"]["upload_folder"]
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Set up logging ---
logger = setup_logger()

# --- Global store for chunks ---
chunks = []

# --- Routes ---
@app.route('/', methods=['GET', 'POST'])
def index():
    global chunks
    if request.method == 'POST':
        uploaded_file = request.files.get('pdf')
        if uploaded_file and uploaded_file.filename:
            filename = secure_filename(uploaded_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(file_path)

            text = extract_text(file_path)
            chunks = chunk_text(text)
            embed_and_add_to_index(chunks)
            pdf_id = store_pdf_metadata(filename)
            logger.info(f"PDF '{filename}' uploaded and embedded.")
            return render_template("index.html", msg="PDF Uploaded", pdf_id=pdf_id)
        else:
            return render_template("index.html", msg="No file selected")
    
    return render_template("index.html")

@app.route('/query', methods=['POST'])
def query():
    global chunks
    user_query = request.form.get("query")
    pdf_id = int(request.form.get("pdf_id", 0))

    results = search_query(user_query, chunks)
    result_text = "\n\n".join(results)
    store_query_result(pdf_id, user_query, result_text)

    logger.info(f"Query '{user_query}' processed for PDF ID {pdf_id}")
    return render_template("index.html", msg="Results", results=results, pdf_id=pdf_id)

# --- Entry Point ---
if __name__ == '__main__':
    app.run(debug=True)
