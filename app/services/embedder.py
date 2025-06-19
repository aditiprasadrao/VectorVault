import os
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def embed_chunks(chunks):
    return [genai.embed_content(model="models/embedding-001", content=c)['embedding'] for c in chunks]

def embed_query(text):
    return genai.embed_content(model="models/embedding-001", content=text)['embedding']
