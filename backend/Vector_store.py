from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Sample text chunks
chunks = [
    "Employees receive 12 casual leaves.",
    "Office working hours are 9 AM to 6 PM.",
    "Employees can work from home with manager approval."
]

# Create embeddings
embeddings = model.encode(chunks)

# Convert to NumPy array
embeddings = np.array(embeddings).astype("float32")

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

# Add embeddings to FAISS
index.add(embeddings)

print("Embeddings stored successfully!")
print("Total vectors:", index.ntotal)