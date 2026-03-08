import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from langchain_huggingface import HuggingFaceEmbeddings

# Load embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load stored embeddings file
with open("syllabus_embeddings.pkl", "rb") as f:
    data = pickle.load(f)

# Store in variables
chunks = data["chunks"]
chunk_embeddings = np.array(data["embeddings"])

print("Loaded chunks:", len(chunks))


def check_syllabus(user_input, threshold=0.60):

    # Convert user question to embedding
    user_embedding = embedding_model.embed_query(user_input)

    user_embedding = np.array(user_embedding).reshape(1, -1)

    # Compute cosine similarity
    scores = cosine_similarity(user_embedding, chunk_embeddings)

    # Get best score
    max_score = scores.max()

    print("Similarity Score:", max_score)

    if max_score >= threshold:
        return True
    else:
        return False


# Example user question
question = input("Enter question: ")

result = check_syllabus(question)

if result:
    print("✅ Question is WITHIN syllabus")
else:
    print("❌ Question is OUTSIDE syllabus")