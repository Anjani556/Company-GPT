from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Company document chunks
chunks = [
    "Employees receive 12 casual leaves.",
    "Office working hours are 9 AM to 6 PM.",
    "Employees can work from home with manager approval."
]

# Create embeddings
embeddings = model.encode(chunks)
embeddings = np.array(embeddings).astype("float32")

# Create FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# User question
query = "How many casual leaves do employees get?"

# Convert question to embedding
query_embedding = model.encode([query]).astype("float32")

# Search the vector database
distance, index_result = index.search(query_embedding, k=1)

# Print the best matching chunk
print("Question:", query)
print("Answer from company documents:")
print(chunks[index_result[0][0]])