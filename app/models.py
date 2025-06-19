from app import db
from datetime import datetime

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    path = db.Column(db.String(255))
    vector_path = db.Column(db.String(255))
    upload_dt = db.Column(db.DateTime, default=datetime.utcnow)
    nlp_entities = db.Column(db.Text)
    topics = db.Column(db.Text)
    sentiment = db.Column(db.Float)
    summary = db.Column(db.Text)

class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'))
    query_text = db.Column(db.Text)
    results = db.Column(db.Text)
    run_dt = db.Column(db.DateTime, default=datetime.utcnow)
