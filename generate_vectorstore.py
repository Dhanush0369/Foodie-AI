import json
from pathlib import Path
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Load JSON files
def load_json_files(data_path):
    documents = []
    for file in Path(data_path).glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            json_data = json.load(f)
            if isinstance(json_data, dict):
                json_data = [json_data]
            for item in json_data:
                content = (
                    f"Restaurant: {item.get('restaurant_name', '')}\n"
                    f"Name: {item.get('name', '')}\n"
                    f"Category: {item.get('category', '')}\n"
                    f"Description: {item.get('description', '')}\n"
                    f"Price: ₹{item.get('price', '')}\n"
                    f"Location: {item.get('location', '')}\n"
                    f"Contact: {item.get('contact', '')}"
                )
                documents.append(Document(page_content=content, metadata=item))
    return documents

# Embedding Model
def get_embedding_model():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Main
DATA_PATH = "data/"
DB_FAISS_PATH = "vectorstore/db_faiss"

documents = load_json_files(DATA_PATH)
embedding_model = get_embedding_model()

# Create FAISS index directly from documents
db = FAISS.from_documents(documents, embedding_model)
db.save_local(DB_FAISS_PATH)

print(f" Vectorstore created at: {DB_FAISS_PATH}")
