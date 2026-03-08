from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
import pickle

# Load embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load syllabus text
with open("syllabus.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Semantic chunking
splitter = SemanticChunker(embeddings)
chunks = splitter.split_text(text)

print("Total chunks:", len(chunks))

# Generate embeddings for chunks
chunk_embeddings = embeddings.embed_documents(chunks)

# Save chunks + embeddings
data = {
    "chunks": chunks,
    "embeddings": chunk_embeddings
}

with open("syllabus_embeddings.pkl", "wb") as f:
    pickle.dump(data, f)

print("Saved embeddings successfully")